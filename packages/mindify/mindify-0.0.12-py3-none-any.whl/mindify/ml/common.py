import os
from typing import Optional, Any, List, Union, Dict, Tuple

import torch.optim.lr_scheduler
import torchmetrics
import torchvision
from pytorch_lightning import seed_everything
from torch import nn
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchmetrics import StatScores, Metric
from torchvision.transforms import ToTensor
from tqdm import tqdm
from transformers import BatchEncoding

DATALOADER = Optional[DataLoader]
STEP_OUTPUT = Any
EPOCH_OUTPUT = List[Any]


class DataModule:
    def __init__(self):
        self.train_ds = None
        self.valid_ds = None
        self.predict_ds = None

    def prepare_data(self, epoch=None):
        pass

    def train_dataloader(self) -> DATALOADER:
        return None

    def valid_dataloader(self) -> DATALOADER:
        return None

    def predict_dataloader(self) -> DATALOADER:
        return None


class NetModule(nn.Module):
    def __init__(self):
        """

        :param module:
        :param criterion:
        :param optimizer: None 不创建，其他调用 (module: NetModule) 返回 optimizer
        :param lr_scheduler: True 自动创建, None 不创建，其他调用 (module: NetModule, optimizer) 返回 scheduler
        """
        super().__init__()

        self.trainer = None

    def forward(self, x):
        return self.module(x)

    def training_epoch_start(self) -> None:
        pass

    def training_step_start(self) -> None:
        pass

    def training_step(self, batch: Any, batch_idx: int) -> STEP_OUTPUT:
        return None

    def training_step_end(self, output: STEP_OUTPUT, metrucs: Dict) -> None:
        pass

    def training_epoch_end(self, outputs: EPOCH_OUTPUT, metrics: Dict) -> None:
        pass

    def validation_epoch_start(self) -> None:
        pass

    def validation_step_start(self) -> None:
        pass

    def validation_step(self, batch: Any, batch_idx: int) -> Optional[STEP_OUTPUT]:
        return None

    def validation_step_end(self, output: STEP_OUTPUT, metrics: Dict) -> None:
        pass

    def validation_epoch_end(self, outputs: EPOCH_OUTPUT, metrics: Dict) -> None:
        pass

    def predicting_epoch_start(self) -> None:
        pass

    def predicting_step_start(self) -> None:
        pass

    def predicting_step(self, batch: Any, batch_idx: int) -> Optional[STEP_OUTPUT]:
        return None

    def predicting_step_end(self, output: STEP_OUTPUT, metrics: Dict) -> None:
        pass

    def predicting_epoch_end(self, outputs: EPOCH_OUTPUT, metrics: Dict) -> None:
        pass

    def optimizer_step(self, optimizer):
        optimizer.step()

    def scheduler_step(self, scheduler, metrics):
        pass

    def scheduler_epoch(self, scheduler, metrics):
        pass

    def get_progress_bar_dict(self):
        tqdm_dict = super().get_progress_bar_dict()
        if 'v_num' in tqdm_dict:
            del tqdm_dict['v_num']

        return tqdm_dict

    def configure_optimizers(self):
        return None

    def log(self, name, value, prog_bar: bool = True, on_global: bool = False):
        self.trainer.log(name, value, prog_bar=prog_bar, on_global=on_global)

    @property
    def current_epoch(self):
        return self.trainer.current_epoch

    @property
    def global_step(self):
        return self.trainer.global_step


class NetTrainer(object):
    def __init__(self, seed=None, reload_dataloader: bool = False, accelerator: str = 'gpu'):
        if seed is not None:
            seed_everything(seed=seed, workers=True)

        self.reload_dataloader = reload_dataloader
        self.accelerator = accelerator
        self.should_stop = False
        self._module = None
        self._datamodule = None
        self._optimizer = None
        self._scheduler = None
        self._global_metrics = {}
        self._epoch_metrics = {}
        self._tqdm_global_metrics = {}
        self._tqdm_epoch_metrics = {}
        self._tqdm: tqdm = None

    @property
    def device(self):
        return 'cuda' if self.accelerator == 'gpu' else 'cpu'

    def convert_batch_to_device(self, batch):
        if isinstance(batch, torch.Tensor) or isinstance(batch, BatchEncoding):
            return batch.to(self.device)
        elif isinstance(batch, Dict):
            return {name: value.to(self.device) for name, value in batch.items()}
        elif isinstance(batch, List):
            return [value.to(self.device) for value in batch]
        else:
            return batch.to(self.device)

    @staticmethod
    def stats_model(model):
        total_params = sum(p.numel() for p in model.parameters()) / 1e6
        print('{:.03f}M total parameters.'.format(total_params))
        total_trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad) / 1e6
        print('{:.03f}M training parameters.'.format(total_trainable_params))

    def log(self, name, value, prog_bar: bool = True, on_global: bool = False):
        if isinstance(value, Metric):
            value = value.compute().item()
        elif isinstance(value, torch.Tensor):
            value = value.item()

        if on_global:
            self._global_metrics[name] = value
        else:
            self._epoch_metrics[name] = value

        if prog_bar:
            if on_global:
                self._tqdm_global_metrics[name] = value
            else:
                self._tqdm_epoch_metrics[name] = value

            self._tqdm.set_postfix(self.tqdm_metrics)

    @property
    def metrics(self):
        return {**self._epoch_metrics, **self._global_metrics}

    @property
    def tqdm_metrics(self):
        return {**self._tqdm_epoch_metrics, **self._tqdm_global_metrics}

    @property
    def optimizer(self):
        return self._optimizer

    @property
    def scheduler(self):
        return self._scheduler

    def save_checkpoint(self, ckpt_path):
        ckpt_parent_path = os.path.dirname(ckpt_path)
        if not os.path.exists(ckpt_parent_path):
            os.makedirs(ckpt_parent_path, exist_ok=True)

        torch.save(self._module.state_dict(), ckpt_path)

    def fit(self, module: NetModule, datamodule, epochs=20, ckpt_path=None):
        self._module = module
        self._datamodule = datamodule

        if ckpt_path is not None:
            self._module.load_state_dict(torch.load(ckpt_path), strict=False)
        self._module.to(self.device)

        self._module.trainer = self

        self._optimizer, self._scheduler = module.configure_optimizers(epochs)

        self.global_step = 0
        self.should_stop = False

        if not self.reload_dataloader:
            self._datamodule.prepare_data(0)
            train_dataloader = self._datamodule.train_dataloader()
            valid_dataloader = self._datamodule.valid_dataloader()

        for epoch in range(epochs):
            self.current_epoch = epoch

            self._epoch_metrics.clear()
            self._tqdm_epoch_metrics.clear()

            if self.reload_dataloader:
                self._datamodule.prepare_data(epoch)
                train_dataloader = self._datamodule.train_dataloader()
                valid_dataloader = self._datamodule.valid_dataloader()

            self.fit_step(self._module, train_dataloader, valid_dataloader, epoch, epochs,
                          self._optimizer, self._scheduler)

    def fit_step(self, module, train_dataloader, valid_dataloader, epoch, epochs, optimizer, scheduler):
        total_len = len(train_dataloader)
        if valid_dataloader is not None:
            total_len += len(valid_dataloader)

        with tqdm(total=total_len) as _tqdm:
            self._tqdm = _tqdm
            self._tqdm.set_description('Epoch [{}/{}]'.format(epoch + 1, epochs))

            module.train()
            module.training_epoch_start()

            if self.should_stop:
                return

            training_outputs = []

            for batch_idx, batch in enumerate(train_dataloader):
                module.zero_grad()
                module.training_step_start()

                if self.should_stop:
                    return

                output = module.training_step(self.convert_batch_to_device(batch), batch_idx)
                training_outputs.append(output)

                if self.should_stop:
                    return

                if isinstance(output, torch.Tensor):
                    loss = output
                elif isinstance(output, Dict):
                    loss = output['loss']
                elif isinstance(output, Tuple) or isinstance(output, List):
                    loss = output[0]

                self.log('loss', loss, prog_bar=True)

                loss.backward()

                module.optimizer_step(optimizer)
                module.scheduler_step(scheduler, self.metrics)
                module.training_step_end(output, self.metrics)

                if self.should_stop:
                    return

                self.global_step += 1

                self._tqdm.set_postfix(self.tqdm_metrics)
                self._tqdm.update(1)

            module.training_epoch_end(training_outputs, self.metrics)

            if self.should_stop:
                return

            if valid_dataloader is not None:
                module.eval()
                with torch.no_grad():
                    module.validation_epoch_start()

                    if self.should_stop:
                        return

                    validation_outputs = []

                    for batch_idx, batch in enumerate(valid_dataloader):
                        module.validation_step_start()

                        if self.should_stop:
                            return

                        output = module.validation_step(self.convert_batch_to_device(batch), batch_idx)
                        validation_outputs.append(output)

                        if self.should_stop:
                            return

                        if isinstance(output, torch.Tensor):
                            loss = output
                        elif isinstance(output, Dict):
                            loss = output['loss']
                        elif isinstance(output, Tuple) or isinstance(output, List):
                            loss = output[0]

                        self.log('val_loss', loss, prog_bar=False)

                        module.validation_step_end(output, self.metrics)

                        if self.should_stop:
                            return

                        self.global_step += 1

                        self._tqdm.set_postfix(self.tqdm_metrics)
                        self._tqdm.update(1)

                    module.validation_epoch_end(validation_outputs, self.metrics)

                if self.should_stop:
                    return

            module.scheduler_epoch(scheduler, self.metrics)

    def predict(self, module, datamodule, ckpt_path=None):
        self._module = module
        self._datamodule = datamodule

        if ckpt_path is not None:
            module.load_state_dict(torch.load(ckpt_path))
        module.to(self.device)
        module.eval()

        module.trainer = self

        datamodule.prepare_data(0)
        predict_dataloader = datamodule.predict_dataloader()
        total_len = len(predict_dataloader)

        self.current_epoch = 0
        self.global_step = 0

        self._epoch_metrics.clear()
        self._tqdm_epoch_metrics.clear()

        with torch.no_grad():
            with tqdm(total=total_len) as _tqdm:
                self._tqdm = _tqdm
                self._tqdm.set_description('Predict')

                module.predicting_epoch_start()

                predicting_outputs = []

                for batch_idx, batch in enumerate(predict_dataloader):
                    module.predicting_step_start()

                    output = module.predicting_step(self.convert_batch_to_device(batch), batch_idx)
                    predicting_outputs.append(output)

                    module.predicting_step_end(output, self.metrics)

                    self.global_step += 1

                    self._tqdm.set_postfix(self.tqdm_metrics)
                    self._tqdm.update(1)

                predicting_outputs = torch.cat(predicting_outputs, dim=0)
                module.predicting_epoch_end(predicting_outputs, self.metrics)

        return predicting_outputs


if __name__ == '__main__':
    class MNISTDataModule(DataModule):
        def __init__(self, batch_size=1024, dataset_path='/resources/data', download: bool = True, **kwargs):
            super().__init__()

            self.batch_size = batch_size
            self.dataset_path = dataset_path
            self.download = download

        def prepare_data(self, epoch=None) -> None:
            self.train_ds = torchvision.datasets.EMNIST(root=self.dataset_path, split='digits', train=True,
                                                        download=False, transform=ToTensor())
            self.valid_ds = torchvision.datasets.EMNIST(root=self.dataset_path, split='digits', train=False,
                                                        download=False, transform=ToTensor())

        def train_dataloader(self) -> DATALOADER:
            return DataLoader(self.train_ds, batch_size=self.batch_size)

        def valid_dataloader(self) -> DATALOADER:
            return DataLoader(self.valid_ds, batch_size=self.batch_size)

        def predict_dataloader(self) -> DATALOADER:
            return DataLoader(self.valid_ds, batch_size=self.batch_size)

    class MNIST(NetModule):
        def __init__(self):
            super().__init__()

            self.classifier = nn.Sequential(
                nn.Flatten(),
                nn.Linear(28*28, 128),
                nn.ReLU(),
                nn.Linear(128, 32),
                nn.ReLU(),
                nn.Linear(32, 10)
            )

            self.criterion = CrossEntropyLoss()

            self.train_loss = torchmetrics.MeanMetric()
            self.train_acc = torchmetrics.Accuracy()
            self.valid_loss = torchmetrics.MeanMetric()
            self.valid_acc = torchmetrics.Accuracy()

        def forward(self, x):
            return self.classifier(x)

        def training_epoch_start(self) -> None:
            self.train_loss.reset()
            self.train_acc.reset()
            self.valid_loss.reset()
            self.valid_acc.reset()

        def training_step(self, batch: Any, batch_idx: int) -> STEP_OUTPUT:
            inputs, labels = batch
            logits = self.classifier(inputs)
            loss = self.criterion(logits, labels)

            self.train_loss.update(loss)
            self.train_acc.update(logits, labels)

            self.log('train_loss', self.train_loss, prog_bar=True)
            self.log('train_acc', self.train_acc, prog_bar=True)

            return loss

        def validation_step(self, batch: Any, batch_idx: int) -> Optional[STEP_OUTPUT]:
            inputs, labels = batch
            logits = self.classifier(inputs)
            loss = self.criterion(logits, labels)

            self.valid_loss.update(loss)
            self.valid_acc.update(logits, labels)

            self.log('valid_loss', self.valid_loss, prog_bar=True)
            self.log('valid_acc', self.valid_acc, prog_bar=True)

            return loss

        def predicting_step(self, batch: Any, batch_idx: int) -> Optional[STEP_OUTPUT]:
            inputs, labels = batch
            logits = self.classifier(inputs)
            logits = torch.argmax(logits, 1)
            return logits

        def configure_optimizers(self, epochs):
            optimizer = Adam(self.parameters(), lr=1e-3)
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3, factor=0.8)

            return optimizer, scheduler

        def scheduler_step(self, scheduler, metrics):
            scheduler.step(metrics['loss'])
            self.log('lr', self.trainer.optimizer.param_groups[0]['lr'], prog_bar=True, on_global=True)

    module = MNIST()
    datamodule = MNISTDataModule(batch_size=2048)

    trainer = NetTrainer(accelerator='gpu')
    trainer.fit(module, datamodule, epochs=5)
