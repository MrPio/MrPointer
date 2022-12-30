import pyautogui

from service.recv_open_handler.recv_open_handler import RecvOpenHandler


class RecvAccelerometer(RecvOpenHandler):
    def __init__(self):
        super().__init__()
        from hardware.mouse.cursor_manager import CursorManager
        self.precision = 2
        self.screen_width, self.screen_height = pyautogui.size()
        self.sensitivity = 22.4
        self.frequency = 0.016
        self.clamp = 1.2e-05
        self.rest_x = 0.0
        self.rest_y = 0.0
        self.rest_z = 0.0
        self.count = 0
        self.sum = 0
        self.compens_z = -0
        self.compens_x = -0
        self.cursor_manager = CursorManager.getInstance()
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.vz: float = 0.0

    def initialize(self, cmd: dict) -> None:
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False
        if 'value' in cmd.keys():
            if cmd['value'] == 'laser':
                self.cursor_manager.change_cursor()

    def process(self, msg: bytes) -> None:
        super().process(msg)
        if self.dt is None or self.dt <= 0:
            return

        ax, ay, az = [float(x) * self.sensitivity for x in msg.decode().split(':')]

        self.vx += ax * self.dt
        self.vy += ay * self.dt
        self.vz += az * self.dt

        self.rest_x += self.vx % 1
        self.rest_y += self.vy % 1
        self.rest_z += self.vz % 1


        vx, vy, vz = self.vx, self.vy, self.vz
        print(vx, vy, vz,self.dt)

        # if self.rest_x // 1 != 0:
        #     vx += self.rest_x // 1
        #     self.rest_x -= self.rest_x // 1
        # if self.rest_y // 1 != 0:
        #     vy += self.rest_y // 1
        #     self.rest_y -= self.rest_y // 1
        # if self.rest_z // 1 != 0:
        #     vz += self.rest_z // 1
        #     self.rest_z -= self.rest_z // 1

        pyautogui.move(vx, vy, duration=0)

    def stop(self) -> None:
        super().stop()
        self.vx, self.vy, self.vz = 0.0, 0.0, 0.0
        self.rest_x = 0.0
        self.rest_y = 0.0
        self.rest_z = 0.0
        if self.cursor_manager.changed:
            self.cursor_manager.restore_cursor()
