import ujson


class DictObject(dict):
    def __init__(self, *args, **kwargs):
        super(DictObject, self).__init__()

        for arg in args:
            if isinstance(arg, dict):
                self.update(arg)
            else:
                raise ValueError('only dict and named arguments accepted')

        self.update(kwargs)

    def replace_key(self, key, new_key):
        new_dict = dict((new_key, v) if k == key else (k, v) for k, v in self.items())

        self.clear()
        self.update(new_dict)

        return self

    def upper_key(self):
        new_dict = dict((k.upper(), v) for k, v in self.items())

        self.clear()
        self.update(new_dict)

        return self

    def lower_key(self):
        new_dict = dict((k.lower(), v) for k, v in self.items())

        self.clear()
        self.update(new_dict)

        return self

    def increase(self, a, inc=1, max=None):
        if a not in self:
            self[a] = inc
        else:
            self[a] += inc

        if max is not None and self[a] > max:
            self[a] = max

        return self

    def decrease(self, a, dec=1, min=None):
        if a not in self:
            self[a] = -dec
        else:
            self[a] -= dec

        if max is not None and self[a] < min:
            self[a] = min

        return self

    def sort_by_values(self, reverse=False):
        new_dict = dict(sorted(self.items(), key=lambda x: x[1], reverse=reverse))

        self.clear()
        self.update(new_dict)

        return self

    def sort_by_keys(self, reverse=False):
        new_dict = dict(sorted(self.items(), key=lambda x: x[0], reverse=reverse))

        self.clear()
        self.update(new_dict)

        return self

    def value_counts(self, objs: list, max=None):
        for obj in objs:
            self.increase(obj, max=max)

        return self

    def __getattr__(self, item):
        if item in self:
            return self.__getitem__(item)
        else:
            return None

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
