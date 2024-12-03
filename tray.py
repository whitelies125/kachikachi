import os
import sys
import subprocess
from PIL import Image
from pystray import Icon, Menu, MenuItem

from thread_manager import threadManager

class Tray:
    def __init__(self):
        self.plot_submenu = Menu(
            MenuItem("today", self.on_plot),
            MenuItem("seven day", self.on_plot),
            MenuItem("this month", self.on_plot),
            MenuItem("this year", self.on_plot),
            MenuItem("all", self.on_plot)
        )
        menu = Menu(
            MenuItem(f"Status: Recording", None),
            MenuItem("Stop record", self.on_stop),
            MenuItem("Plot", self.plot_submenu),
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
            MenuItem("Plot", self.plot_submenu),
            MenuItem("Exit", self.on_exit)
        )

    def on_continue(self, icon, item):
        threadManager.record_event.set()
        icon.menu = Menu(
            MenuItem("Status: Recording", None),
            MenuItem("Stop record", self.on_stop),
            MenuItem("Plot", self.plot_submenu),
            MenuItem("Exit", self.on_exit)
        )

    def on_exit(self, icon, item):
        threadManager.exit_event.set()
        self.icon.stop()

    def on_plot(self, icon, item):
        para = '-all'
        if item == 'today': para = '-today'
        if item == 'seven day': para = '-seven_day'
        if item == 'this month': para = '-month'
        if item == 'this year': para = '-year'
        if item == 'all': para = '-all'
        subprocess.Popen([sys.executable, 'plot.py', para])

    def run(self):
        self.icon.run()

trayInst = Tray()
