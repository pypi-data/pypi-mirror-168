import sys
import time

import pytorch_lightning as pl
from pytorch_lightning.callbacks import ProgressBarBase


class PlainProgressBar(ProgressBarBase):
    def __init__(self):
        super().__init__()
        self.epoch_start_time = time.time()

    def on_train_epoch_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        super().on_train_epoch_start(trainer, pl_module)
        self.epoch_start_time = time.time()

    def on_train_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        super().on_train_epoch_end(trainer, pl_module)

        metrics = trainer.callback_metrics
        metrics = " ".join(
            ['{}={:.04f}'.format(name, float(value)) for name, value in metrics.items() if name != 'v_num'])

        time_cost = time.time() - self.epoch_start_time
        batches_per_second = self.total_batches_current_epoch / time_cost

        sys.stdout.write(f'Epoch [{trainer.current_epoch}/{trainer.fit_loop.max_epochs}] {time_cost:.02f}s bs={self.total_batches_current_epoch} {batches_per_second:.02f}bs/s  {metrics}\n')