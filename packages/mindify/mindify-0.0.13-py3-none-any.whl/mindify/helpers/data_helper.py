import json
import re

import pandas as pd
import numpy as np

from mindify.helpers.dict_object import DictObject


class DataHelper:
    @staticmethod
    def delete_none(_dict):
        if not isinstance(_dict, dict):
            return _dict

        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                DataHelper.delete_none(value)
            elif value is None:
                del _dict[key]
            elif isinstance(value, list):
                for v_i in value:
                    DataHelper.delete_none(v_i)

        return _dict

    @staticmethod
    def convert_to_bool(value):
        if isinstance(value, bool):
            return value

        if isinstance(value, int):
            return value != 0

        if isinstance(value, float):
            return value != 0.0

        if isinstance(value, str):
            return value not in ['False', 'false', 'na', 'No', 'no', 'Off', 'off', '0']

        return not pd.isnull(value)

    @staticmethod
    def print_dataframe(df, full=True):
        if not full:
            print(df)
            return

        config_items = {
            'display.max_columns': None,
            'display.max_rows': None,
            'display.width': None,
            'display.max_colwidth': None,
            'display.float_format': '{:.3f}'.format
        }

        old_configs = {}
        for config_item, config_value in config_items.items():
            old_configs[config_item] = pd.get_option(config_item)
            pd.set_option(config_item, config_value)

        print(df)

        for config_item, config_value in config_items.items():
            pd.set_option(config_item, old_configs[config_item])

    @classmethod
    def dict_to_object(cls, o: dict):
        return DictObject(o)

    @classmethod
    def parse_options(cls, options):
        if pd.isnull(options):
            return None

        if isinstance(options, dict):
            # must be dict like
            return {float(key): value for key, value in options.items()}

        if len(options) == 0:
            return None

        if options[0] == '{':
            # json string like, {"1.0": "1=xxx", "2.0": "2=xxxx"}
            try:
                options = json.loads(options)
                if len(options) == 0:
                    return None
                else:
                    return {float(key): value for key, value in options.items()}
            except:
                return None

        # ; splitted like, "xxxxx;1=yyyyy;2-zzzzzz"
        options_array = options.split(';')
        options_array = [o.strip() for o in options_array if len(o.strip()) != 0]

        if len(options_array) == 0:
            return None

        if len(options_array) == 1:
            # switch field type, 1=True
            return {0.0: "not " + options_array[0], 1.0: options_array[0]}

        options = {}
        for option in options_array:
            if '=' in option:
                pos = option.index('=')
                options[float(option[:pos])] = option
            elif '-' in option:
                pos = option.index('-')
                options[float(option[:pos])] = option
            elif u'＝' in option:
                pos = option.index(u'＝')
                options[float(option[:pos])] = option
            else:
                options[0.0] = option

        return options if len(options) > 1 else None

    @classmethod
    def format_value(cls, value, format_str):
        if format_str is None:
            format_str = "{}"

        if isinstance(format_str, str):
            format_str = [format_str, ""]

        if pd.isnull(value):
            return format_str[1]

        try:
            if format_str[0][0] == '{':
                return format_str[0].format(value)
            else:
                return value.strftime(format_str[0])
        except:
            return format_str[1]

    @classmethod
    def is_idcard(cls, x):
        """
        是否是身份证号
        :param x:
        :return:
        """
        try:
            return 1 if len(str(x)) == 18 or len(str(x)) == 15 else 0
        except:
            return 0

    def is_phone_number(x):
        """
        是否是手机号码
        :param cls:
        :param x:
        :return:
        """
        try:
            return 1 if re.match(r'^1[0-9]{10}$', str(x)) else 0
        except:
            return 0

    @classmethod
    def is_datetime(cls, x):
        """
        日期+时间类型
        :param cls:
        :param x:
        :return:
        """
        try:
            return 1 if re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}(:[0-9]{2}(:[0-9]{2})?)?$', str(x)) else 0
        except:
            return 0

    @classmethod
    def is_date(cls, x):
        """
        日期类型
        :param cls:
        :param x:
        :return:
        """
        try:
            return 1 if re.match(r'^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$', str(x)) else 0
        except:
            return 0

    @classmethod
    def is_time(cls, x):
        """
        时间类型
        :param cls:
        :param x:
        :return:
        """
        try:
            return 1 if re.match(r'^[0-9]{2}:[0-9]{2}(:[0-9]{2})?$', str(x)) else 0
        except:
            return 0

    @classmethod
    def is_integer(cls, x):
        """
        整形数字
        :param cls:
        :param x:
        :return:
        """
        try:
            return 1 if re.match(r'^[-]?[1-9][0-9]*$', str(x)) else 0
        except:
            return 0

    @classmethod
    def is_float(cls, x):
        """
        浮点数字
        :param cls:
        :param x:
        :return:
        """
        try:
            return 1 if re.match(r'^[-]?[0-9]+(\.[0-9]+)?$', str(x)) else 0
        except:
            return 0

    @classmethod
    def remove_csv_quote(cls, v):
        if v[0] == '=':
            v = v[2:-1]
            if len(v) == 0:
                return None
            else:
                return v
        else:
            return v

    @classmethod
    def sort_dict_by_key(cls, a, reverse=False):
        return {k: v for k, v in sorted(a.items(), key=lambda x: x[0], reverse=reverse)}

    @classmethod
    def sort_dict_by_value(cls, a, reverse=False):
        return {k: v for k, v in sorted(a.items(), key=lambda x: x[1], reverse=reverse)}

    @classmethod
    def batches(cls, iterable: list, n: int = 50) -> list:
        length = len(iterable)

        for index in range(0, length, n):
            yield iterable[index: min(index + n, length)]

    @classmethod
    def rolling_window(cls, a, window):
        for idx in range(0, len(a) - window + 1):
            yield a[idx:idx+window]


if __name__ == "__main__":
    for a in DataHelper.batches(range(0, 100), 11):
        print(a)

    for a in DataHelper.rolling_window([1,2,3,4,5,6,7], window=7):
        print(a)
