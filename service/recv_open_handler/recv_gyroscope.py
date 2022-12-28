import pyautogui


from service.recv_open_handler.recv_open_handler import RecvOpenHandler


class RecvGyroscope(RecvOpenHandler):
    def __init__(self):
        from hardware.mouse.cursor_manager import CursorManager
        self.precision = 2
        self.screen_width, self.screen_height = pyautogui.size()
        self.frequency = 0.016
        self.sensitivity = 1400
        self.clamp = 1.2e-05
        self.rest_z = 0
        self.rest_x = 0
        self.count = 0
        self.sum = 0
        self.compens_z = -0.0183
        self.compens_x = -0.0164
        self.cursor_manager = CursorManager.getInstance()

    def initialize(self,cmd: dict) -> None:
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False
        if 'value' in cmd.keys():
            if cmd['value']=='laser':
                self.cursor_manager.change_cursor()


    def process(self, msg: bytes) -> None:
        x, y, z = [float(x) for x in msg.decode().split(':')]
        val_z = -(z - self.compens_z) * self.sensitivity * self.frequency
        val_x = -(x - self.compens_x) * self.sensitivity * self.frequency

        self.rest_z += val_z % 1
        self.rest_x += val_x % 1

        if self.rest_z // 1 != 0:
            val_z += self.rest_z // 1
            self.rest_z -= self.rest_z // 1
        if self.rest_x // 1 != 0:
            val_x += self.rest_x // 1
            self.rest_x -= self.rest_x // 1
        sign_z=1 if val_z>0 else -1
        sign_x = 1 if val_x > 0 else -1
        # pyautogui.move(((abs(val_z)/10)**0.9)*10*sign_z, ((abs(val_x)/10)**0.9)*10*sign_x, duration=self.frequency)
        pyautogui.move(val_z,val_x, duration=self.frequency)


    def stop(self) -> None:
        from hardware.mouse.cursor_manager import CursorManager
        if self.cursor_manager.changed:
            self.cursor_manager.restore_cursor()
