import html
import json
import os
import re
from hashlib import md5 as hashlib_md5


class TextHelper:
    @staticmethod
    def repeat(str, n: int):
        return "".join([str] * n)

    @staticmethod
    def html_unescape(text):
        if isinstance(text, str):
            return html.unescape(text)
        elif isinstance(text, list):
            return [TextHelper.html_unescape(t) for t in text]
        elif isinstance(text, dict):
            return {key: TextHelper.html_unescape(t) for key, t in text.items()}
        else:
            return text

    @staticmethod
    def trim(text):
        return text.strip()

    @staticmethod
    def md5(text):
        return hashlib_md5(text.encode('utf8')).hexdigest()

    @staticmethod
    def filter(text, punctuation=None, lower=True, nodigit=True):
        if punctuation is None:
            punctuation = '#!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@\n\r\t'

        if lower:
            text = text.lower()

        text = re.sub('[' + punctuation + ']+', ' ', text)
        text = re.sub('\s+', ' ', text)

        if nodigit:
            text = re.sub('([0-9]+)', '', text)

        return text

    @staticmethod
    def camel_to_underscore(string: str):
        return re.sub('([a-z]+)([A-Z])', r'\1_\2', string).lower()

    @staticmethod
    def has_chinese(check_str):
        """
        判断字符串中是否包含中文
        :param check_str: {str} 需要检测的字符串
        :return: {bool} 包含返回True， 不包含返回False
        """
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False


if __name__ == '__main__':
    import numpy as np
    print(np.random.randint(10, size=3))