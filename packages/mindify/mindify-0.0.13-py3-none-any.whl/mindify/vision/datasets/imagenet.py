from typing import Optional

import torchvision

from mindify.ml.common import DataModule


class ImageNet(DataModule):
    def __init__(self, dataset_path='/resources/data', download: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.dataset_path = dataset_path
        self.download = download

    def prepare_data(self) -> None:
        torchvision.datasets.ImageNet(root=self.dataset_path, download=self.download)

    def setup(self, stage: Optional[str] = None) -> None:
        self.train_ds = torchvision.datasets.ImageNet(root=self.dataset_path, train=True,
                                                    download=False, transform=self.train_transform)
        self.valid_ds = torchvision.datasets.ImageNet(root=self.dataset_path, train=False,
                                                    download=False, transform=self.valid_transform)


if __name__ == '__main__':
    datamodule = ImageNet()
    datamodule.describe()