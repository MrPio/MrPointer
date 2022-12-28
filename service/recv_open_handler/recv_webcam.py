import io

# import cv2
# import numpy
from PIL import Image

from service.recv_open_handler.recv_open_handler import RecvOpenHandler


class RecvWebcam(RecvOpenHandler):

    def process(self, msg: bytes) -> None:
        imageStream = io.BytesIO(msg)
        img = Image.open(imageStream)
        # cv2.imshow('webcam', cv2.resize(cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR), (1280, 720)) )
        # if cv2.waitKey(1) in [ord('q'), 27]:
        #     self.stop()

    def stop(self) -> None:
        print('*** stop recv_webcam ***')
        # cv2.destroyAllWindows()
