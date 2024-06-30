from abc import ABC, abstractmethod


class AbstractDatabase(ABC):

    @abstractmethod
    def insert(self, data):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_all_by_date(self, date):
        raise NotImplementedError

    @abstractmethod
    def get_connection(self):
        raise NotImplementedError

    @abstractmethod
    def get_cursor(self):
        raise NotImplementedError
