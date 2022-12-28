from service.command.command import Command


class LaserPower(Command):
    def execute(self, cmd: dict):
        from hardware.mouse.cursor_manager import CursorManager
        super().execute(cmd)
        if cmd['value']=='normal':
            CursorManager.getInstance().cursor_file='cursor.cur'
            CursorManager.getInstance().change_cursor()
        elif cmd['value']=='strong':
            CursorManager.getInstance().cursor_file='cursor_strong.cur'
            CursorManager.getInstance().change_cursor()