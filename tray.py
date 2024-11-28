import os
import sys
import subprocess
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

from plot import plot
from thread_manager import threadManager

class Tray:
    def __init__(self):
        menu = Menu(
            MenuItem(f"Status: Recording", None),
            MenuItem("Stop record", self.on_stop),
            MenuItem("Plot", self.on_plot),
            MenuItem("Exit", self.on_exit)
        )
        self.icon = Icon("kachikachi", self.create_image(), "Kachikachi", menu = menu)

    def create_image(self):
        path  = os.path.dirname(__file__)
        image_path = os.path.join(path, "clock_icon_64x64.ico")
        image = Image.open(image_path)
        return image

    def on_stop(self, icon, item):
        threadManager.record_event.clear()
        icon.menu = Menu(
            MenuItem("Status: Stopping", None),
            MenuItem("Continue record", self.on_continue),
            MenuItem("Plot", self.on_plot),
            MenuItem("Exit", self.on_exit)
        )

    def on_continue(self, icon, item):
        threadManager.record_event.set()
        icon.menu = Menu(
            MenuItem("Status: Recording", None),
            MenuItem("Stop record", self.on_stop),
            MenuItem("Plot", self.on_plot),
            MenuItem("Exit", self.on_exit)
        )

    def on_exit(self, icon, item):
        threadManager.exit_event.set()
        self.icon.stop()

    def on_plot(self, icon, item):
        subprocess.Popen([sys.executable, 'plot.py'])

    def run(self):
        self.icon.run()

trayInst = Tray()
