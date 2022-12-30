import pyaudio

from service.recv_open_handler.recv_open_handler import RecvOpenHandler


class RecvMicrophone(RecvOpenHandler):
    def __init__(self):
        super().__init__()
        self.pyaudio = pyaudio.PyAudio()
        self.stream: pyaudio.Stream | None = None

    def initialize(self,cmd: dict) -> None:
        self.stream = self.pyaudio.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=44100,
                                        output=True)

    def process(self, msg: bytes) -> None:
        super().process(msg)
        self.stream.write(msg)
        print(len(msg))

    def stop(self) -> None:
        super().stop()
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
