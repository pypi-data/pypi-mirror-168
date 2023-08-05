import zipfile

import kaggle, os


def download_and_decompress(competition, path):
    kaggle.api.competition_download_files(competition, path)

    competition_path = os.path.join(path, competition)
    competition_file = os.path.join(path, competition + ".zip")

    if not os.path.exists(competition_path):
        zip_file = zipfile.ZipFile(competition_file)
        zip_file.extractall(competition_path)

    for file in os.listdir(competition_path):
        if not file.lower().endswith(".zip"):
            continue

        file_path = os.path.join(competition_path, file[:-4])
        if os.path.exists(file_path):
            continue

        file_file = os.path.join(competition_path, file)

        zip_file = zipfile.ZipFile(file_file)
        zip_file.extractall(file_path)


if __name__ == "__main__":
    download_and_decompress('imagenet-object-localization-challenge', '/resources/data/kaggle')