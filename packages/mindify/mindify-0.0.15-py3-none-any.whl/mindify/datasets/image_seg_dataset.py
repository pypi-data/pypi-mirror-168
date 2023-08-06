import cv2, os
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader


class ImageSegDataset(Dataset):
    def __init__(self, image_files, mask_files, transforms, channels=3):
        self.image_files = image_files
        self.mask_files = mask_files
        self.transforms = transforms
        self.channels = channels

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image = cv2.imread(self.image_files[idx])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(self.mask_files[idx], 0) if self.mask_files is not None else None

        if self.transforms is not None:
            image = self.transforms(image)
            mask = self.transforms(mask) if mask is not None else None

        # 灰度图片取第一个通道即可
        if self.channels == 3:
            return (image, mask)
        else:
            return (image[0:1, :, :], mask)

    # @staticmethod
    # def load(dataset_path, test_split=0.15, random_state=7, image_size=(128, 128)):
    #     assert os.path.exists(dataset_path)
    #
    #     # define the path to the images and masks dataset
    #     image_dataset_path = os.path.join(dataset_path, "images")
    #     mask_dataset_path = os.path.join(dataset_path, "masks")
    #     assert os.path.exists(image_dataset_path) and os.path.exists(mask_dataset_path)
    #
    #     image_files = sorted(list(paths.list_images(image_dataset_path)))
    #     mask_files = sorted(list(paths.list_images(mask_dataset_path)))
    #     assert len(image_files) == len(mask_files)
    #
    #     X_train, X_test, y_train, y_test = train_test_split(
    #         image_files, mask_files, test_size=test_split, random_state=random_state)
    #
    #     compose_transforms = transforms.Compose([
    #         transforms.ToPILImage(),
    #         transforms.Resize(image_size),
    #         transforms.ToTensor()])
    #
    #     train_dataset = ImageSegDataset(image_files=X_train, mask_files=y_train, transforms=compose_transforms)
    #     test_dataset = ImageSegDataset(image_files=X_test, mask_files=y_test, transforms=compose_transforms)
    #     print(f"[INFO] found {len(train_dataset)} examples in the training set...")
    #     print(f"[INFO] found {len(test_dataset)} examples in the test set...")
    #
    #     return train_dataset, test_dataset
