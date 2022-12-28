import json

import websocket
import winotify
from PIL import Image

url = 'wss://mrpio-mrpowermanager.onrender.com/ws/'
local_url = 'ws://localhost:8000/ws/'


class WebsocketManager:

    def __init__(self,
                 trace: bool = True):
        self.on_message: 'function[bytes]' = lambda _: None
        websocket.enableTrace(trace)
        self.is_connected=False


    def connect(self, token:str):
        self.ws = websocket.WebSocketApp(
            url=url + token,
            on_open=lambda _: self.__on_open(),
            on_message=lambda _, msg: self.__on_message(msg),
            on_error=lambda _, err: self.__on_error(err),
            on_close=lambda _: self.__on_close(),
        )
        self.is_connected=True

        from main import ICON_FOLDER
        notifica = winotify.Notification(
            app_id='MrPointer',
            title='Connection established',
            msg=f'Connected to the token {token}.',
            icon=ICON_FOLDER + '/icon.ico',
            duration='short',
        )
        notifica.set_audio(winotify.audio.Default, False)
        notifica.show()

        self.ws.run_forever()

    def disconnect(self):
        self.is_connected=False
        self.ws.close()

    def send_string(self, msg: str):
        self.ws.send(msg.encode(), websocket.ABNF.OPCODE_BINARY)

    def send_json(self, msg: dict):
        msg_str = json.dumps(msg)
        self.send_string(msg_str)

    def send_bytes(self, msg: bytes):
        self.ws.send(msg, websocket.ABNF.OPCODE_BINARY)

    def __on_open(self):
        self.send_string('pc online')

    def __on_message(self, msg: bytes):
        self.on_message(msg)

    def __on_error(self, err):
        print(err)

    def __on_close(self):
        print("### closed ###")
