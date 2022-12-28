import abc


class SendCloseHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send_start(self) -> dict:
        pass

    @abc.abstractmethod
    def send(self) -> bytes:
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        pass
