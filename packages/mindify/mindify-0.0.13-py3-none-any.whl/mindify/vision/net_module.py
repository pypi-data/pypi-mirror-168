import os, shortuuid
import tempfile
import uuid
from functools import partial
from typing import Any, Optional, Union, List, Callable

import torch.optim.lr_scheduler
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.optim.lr_scheduler import ReduceLROnPlateau
import torchmetrics
import wandb
from pytorch_lightning import LightningModule, seed_everything, Trainer, Callback
from pytorch_lightning.loggers import WandbLogger, MLFlowLogger, TensorBoardLogger
from pytorch_lightning.loops import FitLoop
from pytorch_lightning.utilities.types import STEP_OUTPUT, EPOCH_OUTPUT
from torch import nn
from torch.nn.modules.loss import _Loss
from torch.optim import Adam, Optimizer
from torch.optim.lr_scheduler import LambdaLR

from mindify.helpers import DateHelper, DictObject
from mindify.helpers.object_helper import ObjectHelper

import warnings

warnings.filterwarnings("ignore")

OptimizerType = Union[str, dict, Optimizer, Callable[[any], Optimizer]]
SchedulerType = Union[str, dict, any, Callable[[any, Optimizer], any]]


class NetModule(LightningModule):
    def __init__(self, module: nn.Module = None,
                 criterion: _Loss = None,
                 top_k: int = 5,
                 optimizer: OptimizerType = 'default',
                 lr_scheduler: SchedulerType = 'default'):
        """

        :param module:
        :param criterion:
        :param optimizer: None 不创建，其他调用 (module: NetModule) 返回 optimizer
        :param lr_scheduler: True 自动创建, None 不创建，其他调用 (module: NetModule, optimizer) 返回 scheduler
        """
        super().__init__()

        self.module = module
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler

        # 注意: CrossEntropyLoss 是softmax 和 负对数损失的结合，所以网络不需要做一次 softmax
        self.criterion = nn.CrossEntropyLoss() if criterion is None else criterion

        # 累计的准确率
        self.train_acc_top1 = torchmetrics.Accuracy(top_k=1)
        self.valid_acc_top1 = torchmetrics.Accuracy(top_k=1)
        self.top_k = top_k

        if self.top_k is not None:
            self.valid_acc_topk = torchmetrics.Accuracy(top_k=self.top_k)
        else:
            self.valid_acc_topk = None

        # 累计的损失
        self.train_loss = torchmetrics.MeanMetric()
        self.valid_loss = torchmetrics.MeanMetric()

    def forward(self, x):
        return self.module(x)

    def training_step(self, batch: Any, batch_idx: int) -> STEP_OUTPUT:
        inputs, targets = batch

        outputs = self.forward(inputs)
        loss = self.criterion(outputs, targets)

        self.train_loss.update(loss)
        self.train_acc_top1.update(outputs, targets)

        # 系统会自动跟踪 loss 值，这里就不用再记录了，但是记录的loss是每个batch的loss，波动很大，不适合观察，我们需要一个平均值
        # 进度条输出累计的准确率和损失, 不需要上传到 wandb。
        self.log('_loss', self.train_loss.compute(), logger=False, prog_bar=True)
        self.log("_acc", self.train_acc_top1.compute(), logger=False, prog_bar=True)

        return loss

    def validation_step(self, batch: Any, batch_idx: int) -> Optional[STEP_OUTPUT]:
        inputs, targets = batch

        outputs = self.forward(inputs)
        loss = self.criterion(outputs, targets)

        self.valid_loss.update(loss)
        self.valid_acc_top1.update(outputs, targets)

        if self.valid_acc_topk is not None:
            self.valid_acc_topk.update(outputs, targets)

        return None

    def training_epoch_end(self, outputs: EPOCH_OUTPUT) -> None:
        self.log("loss", self.train_loss.compute(), on_epoch=True)
        self.log("acc", self.train_acc_top1.compute(), on_epoch=True)
        self.train_loss.reset()
        self.train_acc_top1.reset()

        optimizer = self.optimizers()
        if isinstance(optimizer, list):
            # 默认只查看第一个group
            optimizer = optimizer[0]
        self.log("lr", optimizer.param_groups[0]['lr'], logger=True, prog_bar=True)

        if self.trainer is not None and self.trainer.train_dataloader is not None:
            dataloader = self.trainer.train_dataloader.loaders
            if isinstance(dataloader, list):
                dataloader = dataloader[0]
            self.log("batch_size", float(dataloader.batch_size), logger=False, prog_bar=True)

    def validation_epoch_end(self, outputs: Union[EPOCH_OUTPUT, List[EPOCH_OUTPUT]], **kwargs) -> None:
        self.log("val_loss", self.valid_loss.compute(), on_epoch=True, prog_bar=True)
        self.log("val_acc", self.valid_acc_top1.compute(), on_epoch=True, prog_bar=True)

        if self.valid_acc_topk is not None:
            self.log(f"val_acc_top{self.top_k}", self.valid_acc_topk.compute(), on_epoch=True, prog_bar=True)

        self.valid_loss.reset()
        self.valid_acc_top1.reset()

        if self.valid_acc_topk is not None:
            self.valid_acc_topk.reset()

    def get_progress_bar_dict(self):
        tqdm_dict = super().get_progress_bar_dict()
        if 'v_num' in tqdm_dict:
            del tqdm_dict['v_num']

        return tqdm_dict

    def configure_optimizers(self):
        if callable(self.optimizer):
            optimizer = self.optimizer(self)
        elif isinstance(self.optimizer, str):
            if self.optimizer == 'default' or self.optimizer == 'adam':
                optimizer = Adam(self.parameters(), lr=0.001)
            else:
                raise f"unknown optimizer {self.optimizer}"
        else:
            optimizer = self.optimizer

        if isinstance(self.lr_scheduler, dict):
            scheduler = self.lr_scheduler
        elif callable(self.lr_scheduler):
            scheduler = self.lr_scheduler(self, optimizer)
        elif isinstance(self.lr_scheduler, str):
            if self.lr_scheduler == 'default' or self.lr_scheduler == 'reducelronplateau':
                scheduler = {
                    'scheduler': ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3, min_lr=1e-8),
                    'monitor': 'loss',
                    "interval": "epoch"
                }
            elif self.lr_scheduler == 'dynamic':
                scheduler = {
                    'scheduler': LambdaLR(optimizer, lr_lambda=self.fetch_dynamic_lr),
                    "interval": "epoch"
                }
            else:
                raise f"unknown lr_scheduler {self.lr_scheduler}"
        else:
            scheduler = self.lr_scheduler

        if scheduler is None:
            return optimizer
        else:
            return {"optimizer": optimizer, "lr_scheduler": scheduler}

    @classmethod
    def fetch_dynamic_lr(cls, step):
        lr_config_file = './.lr.spec'
        if not os.path.exists(lr_config_file):
            return 1.0

        with open(lr_config_file, 'r') as fp:
            lr_str = fp.read()
            return float(lr_str) if lr_str != "" else 1.0


class NetTrainer(object):
    def __init__(self, project: str = 'test', name: str = 'test',
                 precision=32, seed=7, limit_train_batches=None, enable_checkpointing=True,
                 callbacks=None, loggers=None, gpu: bool = True, wandb_enabled: bool = False,
                 hparams=None, accumulate_grad_batches=None, enable_checkpoint: bool = False):
        if hparams is None:
            hparams = dict()
        os.environ["WANDB_NOTEBOOK_NAME"] = name
        seed_everything(seed=seed, workers=True)

        uname = name + "_" + DateHelper.format_date(DateHelper.now(), '%m%d%H%M%S')

        wandb_logger_dir = os.path.join(tempfile.tempdir, "wandb")
        print("wandb_logger_dir = ", wandb_logger_dir)

        if loggers is None:
            loggers = []

        if wandb_enabled:
            loggers.append(WandbLogger(project=project, name=uname, id=uuid.uuid4().hex, dir=wandb_logger_dir,
                                       settings=wandb.Settings(start_method='thread', _disable_stats=True),
                                       reinit=True))

            os.environ["WANDB_NOTEBOOK_NAME"] = project

        if callbacks is None:
            callbacks = []

        if enable_checkpoint:
            checkpoint_callback = ModelCheckpoint(
                monitor='val_loss',
                dirpath=os.path.join(tempfile.tempdir, "checkpoints-" + project),
                filename=project + '-' + name + '-epoch{epoch:02d}-val_loss{val_loss:.4f}',
                save_top_k=5,
                auto_insert_metric_name=False
            )
            callbacks.append(checkpoint_callback)

        self.trainer = Trainer(max_epochs=-1, accelerator='gpu' if gpu else 'cpu',
                               precision=precision,
                               callbacks=callbacks,
                               limit_train_batches=limit_train_batches,
                               accumulate_grad_batches=accumulate_grad_batches,
                               logger=loggers)

        for logger in self.trainer.loggers:
            logger.log_hyperparams({'precision': precision})
            logger.log_hyperparams(hparams)

        self.module = None

    def fit(self, module, datamodule, epochs=20, ckpt_path=None):
        if not isinstance(module, LightningModule):
            module = NetModule(module)

        self.module = module

        self.trainer.fit_loop = FitLoop(max_epochs=epochs)
        self.trainer.fit(module, datamodule, ckpt_path=ckpt_path)

        wandb.finish(quiet=True)
