import time
import ctypes
import logging
import threading
import subprocess
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

from kachikachi import kachikachi
from plot import plot
from shutdown_listener import ShutdownListener


def create_image():
    """生成一个简单的图标图片"""
    width = 64
    height = 64
    color1 = "blue"
    color2 = "white"

    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)
    draw.ellipse((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=color2)
    return image

def on_stop(icon, item):
    record_event.clear()
    icon.menu = Menu(
        MenuItem(f"Status: Stopping", None),
        MenuItem("Continue record", on_continue),
        MenuItem("Plot", on_plot),
        MenuItem("Exit", on_exit)
    )

def on_continue(icon, item):
    record_event.set()
    icon.menu = Menu(
        MenuItem(f"Status: Recording", None),
        MenuItem("Stop record", on_stop),
        MenuItem("Plot", on_plot),
        MenuItem("Exit", on_exit)
    )

def on_exit(icon, item):
    exit_event.set()
    icon.stop()

def on_plot(icon, item):
    subprocess.Popen(['./Scripts/python', 'plot.py'])

def listen_for_shutdown(icon):
    shutdownListener = ShutdownListener(icon, [exit_event])
    shutdownListener.run()

def main():
    logging.basicConfig(
        filename = "tray_log.txt",  # 日志文件名
        level = logging.INFO,  # 设置最低记录级别
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        filemode = "w",  # 写入模式：'w' 覆盖，'a' 追加
    )

    global record_event
    global exit_event
    record_event = threading.Event()
    exit_event = threading.Event()
    record_event.set()
    # 启动后台线程
    # deamen = False, 主线程等待子线程退出后才退出
    threading.Thread(target = kachikachi, args = (record_event, exit_event), daemon = False).start()

    # 创建菜单
    menu = Menu(
        MenuItem(f"Status: Recording", None),
        MenuItem("Stop record", on_stop),
        MenuItem("Plot", on_plot),
        MenuItem("Exit", on_exit)
    )
    # 创建托盘程序
    icon = Icon("kachikachi", create_image(), "Kachikachi", menu=menu)

    # 启动后台线程来监听关机事件
    # deamen = True, 主线程退出时强制终止子线程
    threading.Thread(target = listen_for_shutdown, args = (icon,), daemon = True).start()

    # 运行托盘程序
    icon.run()

if __name__ == "__main__":
    main()
