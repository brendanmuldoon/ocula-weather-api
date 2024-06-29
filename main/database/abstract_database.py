from abc import ABC, abstractmethod


class AbstractDatabase(ABC):

    @abstractmethod
    def insert(self, data):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError
