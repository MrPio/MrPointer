from hardware.webcam.webcam_manger import WebcamManager
from service.send_open_handler.send_open_handler import SendOpenHandler


class SendWebcam(SendOpenHandler):
    def __init__(self):
        super().__init__()
        self.webcam_manager = WebcamManager()

    def send_start(self) -> dict:
        cmd = {
            'type': 'command',
            'command_type': 'recv',
            'stream_type': 'open',
            'command_name': 'WEBCAM_RECV'
        }
        return cmd

    def send(self) -> bytes:
        return self.webcam_manager.get_image()

    def stop(self) -> None:
        self.webcam_manager.close()
