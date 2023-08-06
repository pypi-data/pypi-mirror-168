from functools import partial
from typing import Union


class ObjectHelper:
    @staticmethod
    def create_object(config: Union[dict, type]):
        if isinstance(config, type):
            return partial(config)()
        else:
            return partial(config.pop("type"), **config)()


if __name__ == '__main__':
    class A:
        def __init__(self, factor):
            self.factor = factor

        def add(self, x, y):
            return x + y + self.factor

    a = ObjectHelper.create_object({"type": A, "factor": 0.1})
    print(a.add(1, 2))
