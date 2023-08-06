import numpy as np
import pandas as pd


class Alphabet:
    def __init__(self):
        self.index2name = {}
        self.name2index = {}
        self.current_index = 0
        self.__frozen = False

    def to_dict(self):
        return dict(
            index2name=self.index2name,
            name2index=self.name2index
        )

    @classmethod
    def load_dict(cls, data, mode='list'):
        """
        load data from data source
        :param data:
        :type data:
        :param mode: list mean {'index2name': [], 'name2index': []}, list means {"aa":1,"bb":2}
        :type mode:
        :return:
        :rtype:
        """
        alphabet = Alphabet()

        if mode == 'list':
            alphabet.index2name = data['index2name']
            alphabet.name2index = data['name2index']
        else:
            alphabet.name2index = data
            alphabet.index2name = {str(index): name for name, index in data.items()}

        alphabet.freeze()
        return alphabet

    def freeze(self):
        self.__frozen = True
        self.index2name["0"] = '<UNK>'
        self.name2index['<UNK>'] = 0

    @property
    def size(self):
        return len(self.index2name)

    @property
    def vocabs(self):
        return list(self.name2index.keys())

    def lookup(self, obj, add_if_not_present=True):
        return self.lookup_index(obj, add_if_not_present=add_if_not_present)

    def lookup_index(self, obj, add_if_not_present=True):
        if isinstance(obj, list) or isinstance(obj, np.ndarray) or isinstance(obj, pd.Series):
            return [self.lookup_index(w, add_if_not_present) for w in list(obj)]

        if obj in self.name2index:
            return self.name2index[obj]
        elif self.__frozen:
            return 0
        elif not add_if_not_present:
            raise ValueError("failed to find " + obj)

        index = self.current_index
        self.current_index += 1

        self.name2index[obj] = index
        self.index2name[str(index)] = obj

        return index

    def lookup_object(self, index):
        index = str(int(index))

        if index not in self.index2name:
            if self.__frozen:
                return self.index2name["0"]
            else:
                raise ValueError("failed to find index " + index)

        return self.index2name[index]

    def lookup_objects(self, indices):
        return [self.lookup_object(index) for index in list(indices)]
