import abc


class ChecksumCheck(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, msg: bytes, checksum: str) -> bool:
        pass
