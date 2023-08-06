from typing import Optional

import torchvision

from mindify.ml.common import DataModule


class CIFAR10(DataModule):
    def __init__(self, dataset_path='/resources/data', download: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.dataset_path = dataset_path
        self.download = download

    def prepare_data(self) -> None:
        torchvision.datasets.CIFAR10(root=self.dataset_path, download=self.download)

    def setup(self, stage: Optional[str] = None) -> None:
        self.train_ds = torchvision.datasets.CIFAR10(root=self.dataset_path, train=True,
                                                     download=False, transform=self.train_transform)
        self.valid_ds = torchvision.datasets.CIFAR10(root=self.dataset_path, train=False,
                                                     download=False, transform=self.valid_transform)


class CIFAR100(DataModule):
    def __init__(self, dataset_path='/resources/data', download: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.dataset_path = dataset_path
        self.download = download

    def prepare_data(self) -> None:
        torchvision.datasets.CIFAR100(root=self.dataset_path, download=self.download)

    def setup(self, stage: Optional[str] = None) -> None:
        self.train_ds = torchvision.datasets.CIFAR100(root=self.dataset_path, train=True,
                                                      download=False, transform=self.train_transform)
        self.valid_ds = torchvision.datasets.CIFAR100(root=self.dataset_path, train=False,
                                                      download=False, transform=self.valid_transform)
