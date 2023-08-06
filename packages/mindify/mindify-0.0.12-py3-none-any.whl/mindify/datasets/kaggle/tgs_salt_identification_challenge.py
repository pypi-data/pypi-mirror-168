import kaggle, os
from imutils import paths
from sklearn.model_selection import train_test_split
import torchvision.transforms as torch_transforms

from mindify.datasets.image_seg_dataset import ImageSegDataset
from mindify.datasets.kaggle.utils import download_and_decompress


def load_dataset(path, valid_split=0.15, random_state=7, transform=None, image_size=None, prepare=False):
    assert os.path.exists(path)

    competition = "tgs-salt-identification-challenge"
    download_and_decompress(competition, path)

    competition_path = os.path.join(path, competition)
    assert os.path.exists(competition_path)

    if prepare:
        return

    competition_data_path = os.path.join(competition_path, "competition_data/competition_data")

    image_dataset_path = os.path.join(competition_data_path, "train/images")
    mask_dataset_path = os.path.join(competition_data_path, "train/masks")
    test_dataset_path = os.path.join(competition_data_path, "test/images")
    assert os.path.exists(image_dataset_path) and os.path.exists(mask_dataset_path) and os.path.exists(test_dataset_path)

    image_files = sorted(list(paths.list_images(image_dataset_path)))
    mask_files = sorted(list(paths.list_images(mask_dataset_path)))
    test_files = sorted(list(paths.list_images(test_dataset_path)))
    assert len(image_files) == len(mask_files)

    compose_transforms = [torch_transforms.ToPILImage()]
    if image_size is not None:
        compose_transforms.append(torch_transforms.Resize(image_size))
    if transform is not None:
        compose_transforms.append(transform)
    compose_transforms.append(torch_transforms.ToTensor())

    compose_transforms = torch_transforms.Compose(compose_transforms)

    if valid_split is None:
        train_dataset = ImageSegDataset(image_files=image_files, mask_files=mask_files, transforms=compose_transforms)
        test_dataset = ImageSegDataset(image_files=test_files, mask_files=None, transforms=compose_transforms)

        print(f"[INFO] found {len(image_files)} examples in the train set...")
        print(f"[INFO] found {len(test_files)} examples in the test set...")

        return train_dataset, None, test_dataset
    else:
        X_train, X_valid, y_train, y_valid = train_test_split(
            image_files, mask_files, test_size=valid_split, random_state=random_state)

        train_dataset = ImageSegDataset(image_files=X_train, mask_files=y_train, transforms=compose_transforms)
        valid_dataset = ImageSegDataset(image_files=X_valid, mask_files=y_valid, transforms=compose_transforms)
        test_dataset = ImageSegDataset(image_files=test_files, mask_files=None, transforms=compose_transforms)

        print(f"[INFO] found {len(train_dataset)} examples in the train set...")
        print(f"[INFO] found {len(valid_dataset)} examples in the valid set...")
        print(f"[INFO] found {len(test_files)} examples in the test set...")

        return train_dataset, valid_dataset, test_dataset