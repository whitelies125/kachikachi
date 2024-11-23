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
        """生成一个简单的图标图片"""
        width = 64
        height = 64
        color1 = "blue"
        color2 = "white"

        image = Image.new("RGB", (width, height), color1)
        draw = ImageDraw.Draw(image)
        draw.ellipse((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=color2)
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
        subprocess.Popen(['./Scripts/python', 'plot.py'])

    def run(self):
        self.icon.run()

trayInst = Tray()
