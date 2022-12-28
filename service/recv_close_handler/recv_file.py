import os
import time
from typing import BinaryIO
import userpaths

from service.recv_close_handler.recv_close_handler import RecvCloseHandler


class RecvFile(RecvCloseHandler):
    def __init__(self):
        super().__init__()
        self.file_writer: BinaryIO | None = None

    def initialize(self, cmd: dict):
        super().initialize(cmd)

        # Prepare the file to fill with bytes
        file_name = cmd['file_name']
        self.pkg_tot = int(cmd['file_packets'])
        if os.path.exists(userpaths.get_desktop() + '\\' + file_name):
            os.remove(userpaths.get_desktop() + '\\' + file_name)
        self.file_writer = open(userpaths.get_desktop() + '\\' + file_name, 'ab')

    def process(self, msg: bytes, checksum: str) -> None:
        # controllo il checksum con quello mandatomi
        from service.main_service import MainService
        if not MainService.checksum_check.check(msg, checksum):
            print('!!!!!!!!!diversi!!!!!!!!!')
            return
        self.pkg_recv += 1

        self.file_writer.write(msg)
        percentage = round(100 * self.pkg_recv / self.pkg_tot, 2)
        print(f'{percentage} %')
        if percentage >= 100:
            self.pkg_recv, self.pkg_tot = 0, 0
            print(f'File closed. took ---> {(time.time_ns() - self.sharing_start) / 1000000} ms')
            self.file_writer.close()
            self.current_command = None

    def stop(self) -> None:
        pass
