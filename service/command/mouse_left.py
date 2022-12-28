from pyautogui import click

from service.command.command import Command


class MouseLeft(Command):
    def execute(self, cmd: dict):
        super().execute(cmd)
        click(button='left')