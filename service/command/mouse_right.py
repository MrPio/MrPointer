from pyautogui import click

from service.command.command import Command


class MouseRight(Command):
    def execute(self, cmd: dict):
        super().execute(cmd)
        click(button='right')