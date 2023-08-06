from typing import Optional

import torchvision

from mindify.ml.common import DataModule


class MNIST(DataModule):
    def __init__(self, dataset_path='/resources/data', download: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.dataset_path = dataset_path
        self.download = download

    def prepare_data(self) -> None:
        torchvision.datasets.EMNIST(root=self.dataset_path, split='digits', download=self.download)

    def setup(self, stage: Optional[str] = None) -> None:
        self.train_ds = torchvision.datasets.EMNIST(root=self.dataset_path, split='digits', train=True,
                                                    download=False, transform=self.train_transform)
        self.valid_ds = torchvision.datasets.EMNIST(root=self.dataset_path, split='digits', train=False,
                                                    download=False, transform=self.valid_transform)


class FashionMNIST(DataModule):
    def __init__(self, dataset_path='/resources/data', download: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.dataset_path = dataset_path
        self.download = download

    def prepare_data(self) -> None:
        torchvision.datasets.FashionMNIST(root=self.dataset_path, download=self.download)

    def setup(self, stage: Optional[str] = None) -> None:
        self.train_ds = torchvision.datasets.FashionMNIST(root=self.dataset_path, train=True,
                                                          download=False, transform=self.train_transform)
        self.valid_ds = torchvision.datasets.FashionMNIST(root=self.dataset_path, train=False,
                                                          download=False, transform=self.valid_transform)


if __name__ == '__main__':
    mnist = FashionMNIST(sampling_rate=0.1)
    mnist.describe()
    mnist.down_sampling()
