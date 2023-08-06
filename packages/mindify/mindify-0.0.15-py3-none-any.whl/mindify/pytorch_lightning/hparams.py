from typing import Union, Dict, List

import numpy as np
from pytorch_lightning.utilities import AttributeDict


class HParamsGenerator:
    def __init__(self, config: Union[Dict, AttributeDict]):
        for name, value in config.items():
            if not isinstance(value, List):
                config[name] = [value]

        self.config = config
        self.hparams_len = np.cumprod([len(v) for n, v in self.config.items()])[-1]

    def __len__(self):
        return self.hparams_len

    def __getitem__(self, index):
        hparams = AttributeDict()

        index = index % self.hparams_len
        for n, v in self.config.items():
            hparams[n] = v[index % len(v)]
            index = index // len(v)

        return hparams
