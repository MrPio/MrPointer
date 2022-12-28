import abc
import time


class RecvCloseHandler(metaclass=abc.ABCMeta):
    def __init__(self):
        self.pkg_recv = 0
        self.pkg_tot = 0
        self.sharing_start:int|None=time.time_ns()

    def initialize(self, cmd: dict):
        self.pkg_recv=0
        self.pkg_tot=0
        self.sharing_start=time.time_ns()

    @abc.abstractmethod
    def process(self, msg: bytes,checksum:str) -> None:
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        pass
