import abc


class BaseTruth(abc.ABC):
    @abc.abstractmethod
    def add(self, item):
        pass

    @abc.abstractmethod
    def get_all(self):
        pass
    