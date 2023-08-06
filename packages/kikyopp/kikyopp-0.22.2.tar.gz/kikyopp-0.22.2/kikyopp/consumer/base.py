from abc import ABCMeta, abstractmethod


class BaseConsumer(metaclass=ABCMeta):
    @abstractmethod
    def run(self, name):
        pass

    @abstractmethod
    def stop(self):
        pass
