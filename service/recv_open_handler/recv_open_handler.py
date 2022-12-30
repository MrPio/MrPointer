import abc
import time


class RecvOpenHandler(metaclass=abc.ABCMeta):
    def __init__(self):
        self.last_pckg: int | None = None
        self.dt: float | None = None

    def initialize(self, cmd: dict) -> None:
        pass

    def process(self, msg: bytes) -> None:
        now = time.time_ns()/1000000000.0
        if self.last_pckg is not None:
            self.dt = now - self.last_pckg
        self.last_pckg = now

    def stop(self) -> None:
        self.last_pckg = None
        self.dt = None
