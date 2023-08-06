import argparse
import datetime
import sqlite3
import uuid
from typing import Callable, List, Any, Optional, Mapping, Sequence, Union, Dict
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from pytorch_lightning import Callback, Trainer
import pytorch_lightning as pl
from pytorch_lightning.loggers import LightningLoggerBase
from pytorch_lightning.utilities.types import STEP_OUTPUT

from mindify.vision import NetTrainer, DataModule
import torch.nn as nn

GeneratorFuncType = Callable[[dict, DataModule, int], nn.Module]

Trainer

class NetTunnerLogger(LightningLoggerBase):
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        if 'epoch' in metrics:
            epoch = metrics.pop('epoch')
        else:
            epoch = -1

        step = -1 if step is None else step

        cursor = self.conn.cursor()
        try:
            for n, v in metrics.items():
                cursor.execute('INSERT INTO metrics (session_id, name, value, epoch, step, created_time) values (?, ?, ?, ?, ?, ?)', (
                    self.session_id, n, v, epoch, step, datetime.datetime.now()
                ))
            self.conn.commit()
        except Exception as ex:
            print(ex)
            cursor.close()

    def log_hyperparams(self, params: argparse.Namespace, *args, **kwargs):
        if not isinstance(params, dict):
            params = params.__dict__

        cursor = self.conn.cursor()
        try:
            for n, v in params.items():
                cursor.execute('INSERT OR REPLACE INTO hparams (session_id, name, value) values (?, ?, ?)', (
                    self.session_id, n, v
                ))
            self.conn.commit()
        except Exception as ex:
            print(ex)
            cursor.close()

    def finalize(self, status: str) -> None:
        if status == 'success':
            status = 1
        else:
            status = 2

        cursor = self.conn.cursor()
        try:
            cursor.execute("update sessions set status = ? where id = ?", (status, self.session_id))
            self.conn.commit()
        except Exception as ex:
            print(ex)
            cursor.close()

        self.conn.close()

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> Union[int, str]:
        return 1

    def __init__(self,
                 project, name,
                 agg_key_funcs: Optional[Mapping[str, Callable[[Sequence[float]], float]]] = None,
                 agg_default_func: Optional[Callable[[Sequence[float]], float]] = None,
                 **kwargs,
                 ):
        super(NetTunnerLogger, self).__init__(agg_key_funcs=agg_key_funcs, agg_default_func=agg_default_func)

        self.session_id = uuid.uuid4().hex
        self.conn = None

        self.project = project
        self._name = name
        self.prepare_database()

    def prepare_database(self):
        self.conn = sqlite3.connect(f'./{self.project}-{self.name}.db')

        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                create table if not exists sessions (
                    id char(36) primary key not null, 
                    project varchar(255) not null default '',
                    name varchar(255) not null default '',
                    status int not null default 0,
                    created_time timestamp,
                    updated_time timestamp
                    )
            ''')

            cursor.execute('''
                create table if not exists hparams (
                    session_id char(36) not null,
                    name varchar(255) not null,
                    value varchar(255) not null,
                    CONSTRAINT uni_name_value UNIQUE (session_id, name, value)
                )
            ''')

            cursor.execute('''
                create table if not exists metrics (
                    session_id char(36) not null,
                    name varchar(255) not null,
                    value float not null,
                    epoch int,
                    step int,
                    created_time timestamp
                )
            ''')

            cursor.execute('insert into sessions (id, project, name, created_time) values (?, ?, ?, ?)', (
                self.session_id, self.project, self.name, datetime.datetime.now()
            ))

            self.conn.commit()
        except Exception as ex:
            print(ex)
            cursor.close()


class NetTunnerCallback(Callback):
    def on_train_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        """ """

    def on_train_batch_end(
            self,
            trainer: "pl.Trainer",
            pl_module: "pl.LightningModule",
            outputs: STEP_OUTPUT,
            batch: Any,
            batch_idx: int,
            unused: int = 0,
    ) -> None:
        """ """

    def on_validation_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        """ """

    def on_validation_batch_end(
            self,
            trainer: "pl.Trainer",
            pl_module: "pl.LightningModule",
            outputs: Optional[STEP_OUTPUT],
            batch: Any,
            batch_idx: int,
            dataloader_idx: int,
    ) -> None:
        """ """


class NetTunner(object):
    def __init__(self, hparams_config: dict, project, name, wandb_enabled: bool = True, start_index=0):
        self.project = project
        self.name = name
        self.wandb_enabled = wandb_enabled
        self.hparams_config = hparams_config
        self.start_index = start_index
        self.hparams_max_count = np.cumprod([len(v) for n, v in hparams_config.items()])[-1]

    def get_hparams(self, hparams_index) -> dict:
        """
        获取当前超参数
        """
        hparams = {}

        index = hparams_index
        for n, v in self.hparams_config.items():
            hparams[n] = v[index % len(v)]
            index = index // len(v)

        return hparams

    def tune(self, generator: GeneratorFuncType, datamodule: DataModule, epochs: int, jobs: int = 0):
        def train_module(hparams, hparams_index):
            print(f"hparams#{hparams_index}", hparams)

            module = generator(hparams, datamodule, epochs)

            tunner_logger = NetTunnerLogger(
                project=self.project,
                name=self.name
            )

            trainer = NetTrainer(project=self.project, name=self.name,
                                 loggers=[tunner_logger],
                                 hparams=hparams,
                                 wandb_enabled=self.wandb_enabled)
            trainer.fit(module, datamodule, epochs=epochs)

            return trainer.trainer.callback_metrics['val_loss']

        if jobs <= 1:
            for hparams_index in range(self.hparams_max_count):
                if hparams_index < self.start_index:
                    continue

                hparams = self.get_hparams(hparams_index)
                train_module(hparams, hparams_index)
        else:
            with ThreadPoolExecutor(max_workers=jobs) as t:
                for hparams_index in range(self.hparams_max_count):
                    if hparams_index < self.start_index:
                        continue

                    hparams = self.get_hparams(hparams_index)
                    t.submit(train_module, hparams, hparams_index)
