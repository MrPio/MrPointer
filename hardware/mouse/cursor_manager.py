import atexit
import ctypes
import os

import win32con
import win32gui

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class CursorManager:
    __key = object()
    __instance: 'CursorManager' = None

    def __init__(self, key):
        assert (key == CursorManager.__key)

        self.cursors_id = [
            32512, 32513, 32650, 32515, 32649, 32651, 32648, 32646, 32643, 32645, 32642, 32644, 32516, 32514
        ]
        self.cursors = []
        self.changed = False
        self.make_backup()
        self.cursor_file = 'cursor.cur'

    @staticmethod
    def getInstance() -> 'CursorManager':
        if CursorManager.__instance is None:
            CursorManager.__instance = CursorManager(key=CursorManager.__key)
        return CursorManager.__instance

    def make_backup(self):
        self.cursors = []
        for id in self.cursors_id:
            cursor = win32gui.LoadImage(0, id, win32con.IMAGE_CURSOR,
                                        0, 0, win32con.LR_SHARED)
            self.cursors.append(ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR,
                                                               0, 0, win32con.LR_COPYFROMRESOURCE))

    def restore_cursor(self):
        self.changed = False

        # restore the old cursor
        print("restore_cursor")
        for i in range(len(self.cursors_id)):
            ctypes.windll.user32.SetSystemCursor(self.cursors[i], self.cursors_id[i])
            ctypes.windll.user32.DestroyCursor(self.cursors[i])
        self.make_backup()

    def change_cursor(self):
        self.changed = True
        # Make sure cursor is restored at the end
        atexit.register(self.restore_cursor)

        # change system cursor
        for id in self.cursors_id:
            print(f'changed --> {id}')
            from main import ICON_FOLDER
            cursor = win32gui.LoadImage(0, ICON_FOLDER + "/" + self.cursor_file, win32con.IMAGE_CURSOR,
                                        0, 0, win32con.LR_LOADFROMFILE)
            ctypes.windll.user32.SetSystemCursor(cursor, id)
            ctypes.windll.user32.DestroyCursor(cursor)
