import os
from pathlib import Path

from .text_helper import TextHelper


class FileHelper(object):
    @classmethod
    def ensure_file_path(cls, file):
        path = os.path.dirname(file)
        if not os.path.exists(path):
            os.makedirs(path, 0o777, exist_ok=True)
        return file

    @classmethod
    def ensure_cache_file(cls, cache_dir, key):
        md5 = TextHelper.md5(key)
        cache_file = os.path.join(cache_dir, md5[-3], md5[-2], md5[-1], md5)
        return cls.ensure_file_path(cache_file)

    @classmethod
    def read_file(cls, file, mode='r', encoding='utf-8'):
        if file is None or not os.path.exists(file):
            return None

        with open(file, mode, encoding=encoding) as fp:
            return fp.read()

    @classmethod
    def write_file(cls, file, content, mode='w', encoding='utf-8'):
        with open(file, mode, encoding=encoding) as fp:
            fp.write(content)

    @classmethod
    def set_mtime(cls, file, modified_time):
        os.utime(file, (modified_time, modified_time))

    @classmethod
    def get_home_path(cls, relative_path):
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        return os.path.join(Path.home(), '.cache', relative_path)

    @classmethod
    def get_home_path(cls, relative_path):
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        return os.path.join(Path.home(), '.cache', relative_path)