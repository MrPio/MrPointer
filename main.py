import os
import sys
import time
from threading import Thread
from tkinter import font, X

import winotify
from PIL import Image
from PIL.ImageTk import PhotoImage
from pystray import Icon, Menu, MenuItem
from service.main_service import MainService
import tkinter as tk
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

mainService = MainService.getInstance()
websocket_manager = mainService.websocket_manager
ICON_FOLDER = os.path.join(sys._MEIPASS, 'static') #ROOT_DIR

def stray_handler(_, item):
    if str(item) == 'Exit':
        mainService.stop_thread()
        if websocket_manager.is_connected:
            websocket_manager.disconnect()
        os._exit(1)

    elif str(item) == 'Connect to a token':
        ws = tk.Tk()
        ws.title('Establish Connection')
        ws.geometry('500x300')
        ws.iconphoto(False, PhotoImage(file=ICON_FOLDER + "\icon.ico"))
        ws.config(bg='#fcba03')
        ws.resizable(False, False)

        screen_width = ws.winfo_screenwidth()
        screen_height = ws.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (500 / 2))
        y_cordinate = int((screen_height / 2) - (300 / 2))

        ws.geometry("{}x{}+{}+{}".format(500, 300, x_cordinate, y_cordinate))

        lframe = tk.LabelFrame(ws, text='Instructions', bg='#fcba03',
                               font=font.Font(family='Helvetica'))
        label = tk.Label(
            lframe,
            bg='#fcba03',
            font=font.Font(family='Helvetica', size=13),
            text='Write here the same token\r\nyou used on the app.'

        )
        label.pack(fill=tk.BOTH, expand=True)
        lframe.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        var = tk.StringVar()
        tk.Label(ws, text='Token:', bg='#fcba03', font=font.Font(family='Helvetica'), ).pack(
            anchor=tk.NW,
            padx=10)
        e_box = tk.Entry(ws, textvar=var, width=80, font=font.Font(family='Helvetica', size=15))
        e_box.pack(fill=X, padx=30)
        e_box.focus_set()

        def connect():
            token = var.get()
            if len(token) < 3:
                notifica = winotify.Notification(
                    app_id='MrPointer',
                    title='Warning',
                    msg='The token must be at least 3 chars long!',
                    icon=ICON_FOLDER + '/icon.ico',
                    duration='short',
                )
                notifica.set_audio(winotify.audio.Default, False)
                notifica.show()
                return
            if websocket_manager.is_connected:
                pystray_icon.icon = Image.open(ICON_FOLDER + "\icon_red.ico")
                websocket_manager.disconnect()
                time.sleep(0.2)
            Thread(target=websocket_manager.connect, args=[token]).start()
            pystray_icon.icon = Image.open(ICON_FOLDER + "\icon_green.ico")
            ws.destroy()

        var_button = tk.StringVar(value='Connect')
        button = tk.Button(ws, textvariable=var_button, bg='#0176AB', activebackground='#fcba03',
                           fg='#ffffff', font=font.Font(family='Helvetica', size=13), command=connect)

        button.pack(pady=30)

        ws.mainloop()


pystray_icon:Icon=Icon(
        'MrPointer',
        Image.open(ICON_FOLDER + "\icon_red.ico"),
        menu=Menu(
            MenuItem('Connect to a token', stray_handler),
            Menu.SEPARATOR,
            MenuItem('Exit', stray_handler),
        )
    )


if __name__ == '__main__':
    pystray_icon.run_detached()
