import pyautogui

from service.recv_open_handler.recv_open_handler import RecvOpenHandler


class RecvAccelerometer(RecvOpenHandler):
    def __init__(self):
        super().__init__()
        from hardware.mouse.cursor_manager import CursorManager
        self.precision = 2
        self.screen_width, self.screen_height = pyautogui.size()
        self.sensitivity = 350
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
        self.brake: bool = False
        self.a_last_max: float = 0.0
        self.a_motion_detector: int = 100
        self.v_motion_detector: int = 20
        self.a_at_motion_detected: float | None = None
        self.brake_activated=False

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
        ay = -ay

        a_magn = self.magnitude([ax, ay])

        if a_magn > self.a_last_max:
            self.a_last_max = a_magn
        # if a_magn < 80:
        #     print('***** brake on *****')
        # self.brake = True

        if abs(ax) > 100:
            self.vx += ax * self.dt
            self.vy += ay * self.dt
            self.vz += az * self.dt

        # if self.brake and self.magnitude([self.vx, self.vy]) < 9999999999:
        #     print('***** BRAKING *****')
        #     self.vx, self.vy, self.vz = 0.0, 0.0, 0.0
        #     self.brake = False

        if self.magnitude([ax, ay]) > 3:
            print(str(round(self.vx, 1)) + ' m/s  -  ' + str(round(ax, 1)) + ' m/s^2 - ' + str(
                round(self.dt * 1000, 1)) + ' s')

        # bounce compensation
        if self.a_at_motion_detected is not None:
            if self.a_at_motion_detected > 0 and (self.brake_activated or self.vx < self.v_motion_detector):
                self.vx = 0.0
                self.brake_activated = True
                print('***** BREAK2 *****')
            elif self.a_at_motion_detected < 0 and (self.brake_activated or self.vx > -self.v_motion_detector):
                self.vx = 0.0
                self.brake_activated=True
                print('***** BREAK3 *****')
            else:
                self.brake_activated = False

        if abs(ax) > self.a_motion_detector and self.a_at_motion_detected is None:
            self.a_at_motion_detected = ax
            print(f'***** a_at_motion_detected = {self.a_at_motion_detected} *****')
        elif abs(ax) < self.a_motion_detector and self.a_at_motion_detected is not None:
            self.a_at_motion_detected = None
            print(f'***** no motion = {ax} *****')

        self.rest_x += self.vx % 1
        self.rest_y += self.vy % 1
        self.rest_z += self.vz % 1

        vx, vy, vz = self.vx, self.vy, self.vz

        # if self.rest_x // 1 != 0:
        #     vx += self.rest_x // 1
        #     self.rest_x -= self.rest_x // 1
        # if self.rest_y // 1 != 0:
        #     vy += self.rest_y // 1
        #     self.rest_y -= self.rest_y // 1
        # if self.rest_z // 1 != 0:
        #     vz += self.rest_z // 1
        #     self.rest_z -= self.rest_z // 1

        pyautogui.move(vx, 0, duration=0)

    def magnitude(self, vect: list):
        return (sum([x ** 2 for x in vect])) ** 0.5

    def stop(self) -> None:
        super().stop()
        self.vx, self.vy, self.vz = 0.0, 0.0, 0.0
        self.rest_x = 0.0
        self.rest_y = 0.0
        self.rest_z = 0.0
        if self.cursor_manager.changed:
            self.cursor_manager.restore_cursor()
