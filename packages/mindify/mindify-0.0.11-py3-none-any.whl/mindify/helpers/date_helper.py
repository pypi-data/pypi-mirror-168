from datetime import date, datetime, timedelta
from typing import Union

import time

MixedDate = Union[str, int, date, datetime, time.struct_time]


class DateHelper:

    @classmethod
    def parse_date(cls, mixed: MixedDate, fmt=None):
        if mixed is None:
            return None

        if isinstance(mixed, date):
            return mixed

        if isinstance(mixed, int):
            return cls.parse_date(time.localtime(mixed), fmt=fmt)

        if isinstance(mixed, time.struct_time):
            return cls.parse_date(datetime(*mixed[:6]))

        if isinstance(mixed, datetime):
            return cls.parse_date(mixed.date())

        if fmt is not None:
            return datetime.strptime(mixed, fmt).date()

        for fmt in ['%Y-%m-%d', '%Y-%m', '%Y%m%d',
                    '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H',
                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M', '%Y-%m-%dT%H']:
            try:
                res = datetime.strptime(mixed, fmt).date()
                if res is not None:
                    return res
            except:
                pass

        return None
        # raise Exception("invalid date format: {}".format(mixed))

    @classmethod
    def parse_datetime(cls, mixed: MixedDate, fmt=None):
        if mixed is None:
            return None

        if isinstance(mixed, datetime):
            return mixed

        try:
            if isinstance(mixed, int):
                return cls.parse_datetime(time.localtime(mixed), fmt=fmt)

            if isinstance(mixed, time.struct_time):
                return cls.parse_datetime(datetime(*mixed[:6]))

            if isinstance(mixed, datetime):
                return cls.parse_datetime(mixed.date())

            if isinstance(mixed, date):
                return cls.parse_datetime(datetime.fromordinal(mixed.toordinal()))
        except:
            return None

        if fmt is not None:
            try:
                return datetime.strptime(mixed, fmt)
            except:
                pass

        for fmt in ['%Y-%m-%d', '%Y-%m', '%Y%m%d',
                    '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H',
                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M', '%Y-%m-%dT%H']:
            try:
                res = datetime.strptime(mixed, fmt)
                if res is not None:
                    return res
            except:
                pass

        return None
        # raise Exception("invalid datetime format: {}".format(mixed))

    @classmethod
    def parse_time(cls, mixed: MixedDate, fmt=None):
        if mixed is None:
            return None

        if isinstance(mixed, datetime):
            return mixed

        try:
            if isinstance(mixed, int):
                return cls.parse_datetime(time.localtime(mixed), fmt=fmt)

            if isinstance(mixed, time.struct_time):
                return cls.parse_datetime(datetime(*mixed[:6]))

            if isinstance(mixed, datetime):
                return cls.parse_datetime(mixed.date())

            if isinstance(mixed, date):
                return cls.parse_datetime(datetime.fromordinal(mixed.toordinal()))
        except:
            return None

        if fmt is not None:
            try:
                return datetime.strptime(mixed, fmt)
            except:
                pass

        for fmt in ['%H:%M:%S', '%H:%M']:
            try:
                res = datetime.strptime(mixed, fmt)
                if res is not None:
                    return res
            except:
                pass

        return None
        # raise Exception("invalid datetime format: {}".format(mixed))

    @classmethod
    def format_date(cls, mixed: MixedDate, fmt='%Y-%m-%d'):
        if mixed is None:
            return None

        try:
            return cls.parse_date(mixed).strftime(fmt)
        except:
            return None

    @classmethod
    def format_datetime(cls, mixed: MixedDate, fmt="%Y-%m-%d %H:%M:%S"):
        if mixed is None:
            return None

        try:
            return cls.parse_datetime(mixed).strftime(fmt)
        except:
            return None

    @classmethod
    def now(cls, days: int = 0, seconds: int = 0):
        return datetime.now() + timedelta(days=days, seconds=seconds)

    @classmethod
    def add_days(cls, mixed: MixedDate, days: int):
        if mixed is None:
            return None

        return cls.parse_date(mixed) + timedelta(days=days)
