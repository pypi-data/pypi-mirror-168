import os
import zipfile
from pathlib import Path

import kaggle


def uncompress_folder(dataset_path):
    for file in os.listdir(dataset_path):
        if not file.lower().endswith(".zip"):
            continue

        extract_path = os.path.join(dataset_path, file[:-4])
        if os.path.exists(extract_path):
            continue

        zip_file = os.path.join(dataset_path, file)

        zip_file = zipfile.ZipFile(zip_file)
        zip_file.extractall(extract_path)


def get_dataset(dataset, unzip=False):
    dataset_path = os.path.join(Path.home(), ".cache/kaggle", dataset)

    api = kaggle.KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=dataset_path, quiet=False, unzip=False)

    if unzip:
        uncompress_folder(dataset_path)

    return dataset_path


def get_competition(competition, unzip=False):
    dataset_path = os.path.join(Path.home(), ".cache/kaggle", competition)

    api = kaggle.KaggleApi()
    api.authenticate()
    api.competition_download_files(competition, dataset_path)

    if unzip:
        uncompress_folder(dataset_path)

    return dataset_path
