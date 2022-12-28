import abc


class Command(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self, cmd: dict):
        pass
