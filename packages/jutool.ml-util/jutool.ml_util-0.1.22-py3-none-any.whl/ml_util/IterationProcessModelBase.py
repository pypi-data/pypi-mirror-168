import abc


class IterationProcessModelBase(metaclass=abc.ABCMeta):
    def __init__(self, name):
        self._name = name

    @property
    def Name(self):
        return self._name

    @abc.abstractmethod
    def call(self, item):
        pass
