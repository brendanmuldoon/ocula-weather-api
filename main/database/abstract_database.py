from abc import ABC


class AbstractDatabase(ABC):

    def insert(self):
        raise NotImplementedError
