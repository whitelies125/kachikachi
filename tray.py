import time
import ctypes
import logging
import threading
import subprocess
import win32api
import win32con
import win32gui
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

# 定义监听消息钩子函数
def wnd_proc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_QUERYENDSESSION:
        print("System prepare shutdown!")
        logging.info(f"System prepare shutdown!")
    if msg == win32con.WM_ENDSESSION:
        print("System is shutting down!")
        logging.info(f"System is shutting down!")
        exit_event.set()
        icon.stop()
        win32gui.PostQuitMessage(0) # 退出消息监听
        return 1  # 返回 1 表示允许关机
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

# 注册窗口类
def create_window():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = wnd_proc
    wc.lpszClassName = "ShutdownListener"
    wc.hInstance = win32api.GetModuleHandle(None)
    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(
        class_atom,  # 注册类的 atom
        "ShutdownListener",  # 窗口标题
        0,  # 窗口样式
        0, 0,  # 窗口位置 (x, y)
        0, 0,  # 窗口尺寸 (width, height)
        0,  # 父窗口句柄
        0,  # 菜单句柄
        wc.hInstance,  # 实例句柄
        None  # 额外的参数
    )
    return hwnd

def listen_for_shutdown():
    hwnd = create_window()
    win32gui.PumpMessages()  # 启动消息监听
    print("quit msg listen")
    logging.info("quit msg listen")
    win32gui.DestroyWindow(hwnd)
    win32gui.UnregisterClass("ShutdownListener", win32api.GetModuleHandle(None))

def main():
    logging.basicConfig(
        filename = "tray_log.txt",  # 日志文件名
        level = logging.INFO,  # 设置最低记录级别
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        filemode = "w",  # 写入模式：'w' 覆盖，'a' 追加
    )

    # 启动后台线程来监听关机事件
    listener_thread = threading.Thread(target=listen_for_shutdown, daemon=True)
    listener_thread.start()

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
    global icon
    icon = Icon("kachikachi", create_image(), "Kachikachi", menu=menu)
    # 运行托盘程序
    icon.run()

if __name__ == "__main__":
    main()
