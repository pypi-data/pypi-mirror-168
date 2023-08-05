import os
import sys
from typing import Optional

import torch
import torchvision
from pytorch_lightning import LightningDataModule
from pytorch_lightning.utilities.types import TRAIN_DATALOADERS, EVAL_DATALOADERS
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader, Subset
from torchvision import transforms


class DataModule(LightningDataModule):
    def __init__(self, batch_size: int = 1024, valid_batch_size: int = None, multiprocess: bool = None,
                 pin_memory: bool = True, enhanced_transform: bool = False,
                 new_size: int = None, expand_channel: bool = False, sampling_rate: float = None,
                 random_erasing_ratio: float = 0):
        super().__init__()

        self.batch_size = batch_size
        self.valid_batch_size = batch_size if valid_batch_size is None else valid_batch_size
        self.multiprocess = sys.platform == 'linux' if multiprocess is None else multiprocess
        self.pin_memory = pin_memory
        self.enhanced_transform = enhanced_transform
        self.new_size = new_size
        self.expand_channel = expand_channel
        self.train_ds = None
        self.valid_ds = None
        self.sampling_rate = sampling_rate
        self.random_erasing_ratio = random_erasing_ratio

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        self.down_sampling()
        return DataLoader(self.train_ds, batch_size=self.batch_size, shuffle=True,
                          pin_memory=self.pin_memory, num_workers=self.num_workers)

    def val_dataloader(self) -> EVAL_DATALOADERS:
        self.down_sampling()
        return DataLoader(self.valid_ds, batch_size=self.valid_batch_size, shuffle=False,
                          pin_memory=self.pin_memory, num_workers=self.num_workers)

    def down_sampling(self):
        if self.sampling_rate is None:
            return

        kfold = KFold(n_splits=int(1 / self.sampling_rate), shuffle=True)

        if self.train_ds is not None and not isinstance(self.train_ds, Subset):
            _, indices = next(kfold.split(self.train_ds.data, self.train_ds.targets))
            self.train_ds = Subset(self.train_ds, indices)

        if self.valid_ds is not None and not isinstance(self.valid_ds, Subset):
            _, indices = next(kfold.split(self.valid_ds.data, self.valid_ds.targets))
            self.valid_ds = Subset(self.valid_ds, indices)

        # self.down_sample = None

    @property
    def train_transform(self):
        composed_transforms = []

        if self.new_size is not None:
            composed_transforms.append(transforms.Resize(self.new_size))

        if self.enhanced_transform:
            # FLips the image w.r.t horizontal axis
            # composed_transforms.append(transforms.RandomHorizontalFlip())
            # Rotates the image to a specified angel
            composed_transforms.append(transforms.RandomRotation(10))
            composed_transforms.append(transforms.RandomAffine(0, shear=10, scale=(0.8, 1.2)))
            # Set the color params
            composed_transforms.append(transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2))

        # convert the image to tensor so that it can work with torch
        composed_transforms.append(transforms.ToTensor())
        # Normalize all the images
        composed_transforms.append(transforms.Normalize(mean=(0.5,), std=(0.5,)))

        if self.enhanced_transform and self.random_erasing_ratio > 0:
            composed_transforms.append(transforms.RandomErasing(p=self.random_erasing_ratio))

        if self.expand_channel:
            composed_transforms.append(transforms.Lambda(lambd=self.expand_channels))

        return transforms.Compose(composed_transforms)

    @property
    def valid_transform(self):
        composed_transforms = []

        if self.new_size is not None:
            composed_transforms.append(transforms.Resize(self.new_size))

        # convert the image to tensor so that it can work with torch
        composed_transforms.append(transforms.ToTensor())
        # Normalize all the images
        composed_transforms.append(transforms.Normalize(mean=(0.5,), std=(0.5,)))

        if self.expand_channel:
            composed_transforms.append(transforms.Lambda(lambd=self.expand_channels))

        return transforms.Compose(composed_transforms)

    @property
    def num_workers(self):
        return os.cpu_count() * 3 // 4 if self.multiprocess else 0

    @classmethod
    def expand_channels(cls, image):
        if image.size(0) > 1:
            image = image[:1, :, :]

        return torch.squeeze(torch.stack([image, image, image], dim=1), 0)

    def describe(self):
        if self.train_ds is None:
            self.prepare_data()
            self.setup()

        print("train samples: {}, valid samples: {}".format(len(self.train_ds), len(self.valid_ds) if self.valid_ds is not None else 0))

        print("data shape", self.train_ds[0][0].size(), "classes", self.train_ds.classes)

