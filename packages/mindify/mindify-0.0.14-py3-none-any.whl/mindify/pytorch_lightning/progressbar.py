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
        trainer.callback_metrics.clear()

    def on_train_batch_end(
        self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", outputs: STEP_OUTPUT, batch: Any, batch_idx: int
    ) -> None:
        super().on_train_batch_end(trainer, pl_module, outputs, batch, batch_idx)
        self.refresh_progressbar(trainer)

    def on_train_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        super().on_train_epoch_end(trainer, pl_module)
        self.refresh_progressbar(trainer)
        sys.stdout.write("\n")

    def refresh_progressbar(self, trainer: "pl.Trainer"):
        metrics = trainer.callback_metrics
        metrics = " ".join(
            ['{}={:.04f}'.format(name, float(value)) for name, value in metrics.items() if name != 'v_num'])

        time_cost = time.time() - self.epoch_start_time
        batches_per_second = self.train_batch_idx / time_cost

        # sys.stdout.flush()
        sys.stdout.write(f'\rEpoch [{trainer.current_epoch}/{trainer.fit_loop.max_epochs}] {time_cost:.02f}s bs={self.train_batch_idx}/{self.total_batches_current_epoch} {batches_per_second:.02f}bs/s  {metrics}')
