from typing import Dict, Optional, Any


class DictObject(Dict):
    def get_or_default(self, key, default, warning=True):
        if key not in self:
            if warning:
                print("Warning", key, "not in dict")
            return default
        else:
            return self[key]

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

    def __getattr__(self, key: str) -> Optional[Any]:
        try:
            return self[key]
        except KeyError as exp:
            raise AttributeError(f'Missing attribute "{key}"') from exp

    def __setattr__(self, key: str, val: Any) -> None:
        self[key] = val

    def __repr__(self) -> str:
        if not len(self):
            return ""
        max_key_length = max(len(str(k)) for k in self)
        tmp_name = "{:" + str(max_key_length + 3) + "s} {}"
        rows = [tmp_name.format(f'"{n}":', self[n]) for n in sorted(self.keys())]
        out = "\n".join(rows)
        return out
