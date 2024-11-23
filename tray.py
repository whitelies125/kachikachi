import time
import logging
import threading
import subprocess
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

from kachikachi import kachikachi
from plot import plot

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

def on_stop(icon, item, stop_event, exit_event):
    print(f"main : {item}")
    stop_event.set()
    icon.menu = Menu(
        MenuItem(f"Status: Stopping", None),
        MenuItem("Continue record", lambda icon, item: on_continue(icon, item, stop_event, exit_event)),
        MenuItem("Plot", on_plot),
        MenuItem("Exit", lambda icon, item: on_exit(icon, item, exit_event))
    )

def on_continue(icon, item, stop_event, exit_event):
    print(f"main : {item}")
    stop_event.clear()
    icon.menu = Menu(
        MenuItem(f"Status: Recording", None),
        MenuItem("Stop record", lambda icon, item: on_stop(icon, item, stop_event, exit_event)),
        MenuItem("Plot", on_plot),
        MenuItem("Exit", lambda icon, item: on_exit(icon, item, exit_event))
    )

def on_exit(icon, item, exit_event):
    print(f"main : {item}")
    exit_event.set()
    icon.stop()

def on_plot(icon, item):
    print(f"main : {item}")
    subprocess.Popen(['./Scripts/python', 'plot.py'])

def main():
    logging.basicConfig(
        filename="tray_log.txt",  # 日志文件名
        level=logging.INFO,  # 设置最低记录级别
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w",  # 写入模式：'w' 覆盖，'a' 追加
    )

    stop_event = threading.Event()
    exit_event = threading.Event()
    # 启动后台线程
    # deamen = False, 主线程等待子线程退出后才退出
    threading.Thread(target = kachikachi, args = (stop_event, exit_event), daemon = False).start()

    # 创建菜单
    menu = Menu(
        MenuItem(f"Status: Recording", None),
        MenuItem("Stop record", lambda icon, item: on_stop(icon, item, stop_event, exit_event)),
        MenuItem("Plot", on_plot),
        MenuItem("Exit", lambda icon, item: on_exit(icon, item, exit_event))
    )
    # 创建托盘图标
    icon = Icon("kachikachi", create_image(), "Kachikachi", menu=menu)
    # 运行托盘图标
    icon.run()

if __name__ == "__main__":
    main()
