import time
import ctypes
import logging
import threading
import subprocess
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

from kachikachi import kachikachi
from plot import plot

record_event = threading.Event()
exit_event = threading.Event()

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

# CTRL_C_EVENT = 0        # 按下ctlr-c
# CTRL_CLOSE_EVENT = 2    # 控制台关闭
# CTRL_LOGOFF_EVENT = 5   # 用户注销
# CTRL_SHUTDOWN_EVENT = 6 # 系统关机
def shutdown_handler(event):
    event_list = {0, 2, 5, 6}
    print(f"event {event}")
    logging.info(f"event {event}")
    if event in event_list:
        exit_event.set()
        return True  # 返回 True 告诉系统信号已处理
    return False

def main():
    logging.basicConfig(
        filename = "tray_log.txt",  # 日志文件名
        level = logging.INFO,  # 设置最低记录级别
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        filemode = "w",  # 写入模式：'w' 覆盖，'a' 追加
    )
    handler_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)
    handler = handler_type(shutdown_handler)
    ctypes.windll.kernel32.SetConsoleCtrlHandler(handler, True)

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
    # 创建托盘图标
    icon = Icon("kachikachi", create_image(), "Kachikachi", menu=menu)
    # 运行托盘图标
    icon.run()

if __name__ == "__main__":
    main()
