import win32api
import win32con
import win32gui
import logging

from thread_manager import threadManager

class ShutdownListener:
    def __init__(self):
        self.hwnd = None
        self.callback = []

    def addCallback(self, callback):
        self.callback.append(callback)

    # 监听消息钩子函数
    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_QUERYENDSESSION:
            print("System prepare shutdown!")
            logging.warn(f"System prepare shutdown!")
        elif msg == win32con.WM_ENDSESSION:
            print("System is shutting down!")
            logging.warn(f"System is shutting down!")
            for func in self.callback:
                func()
            win32gui.PostQuitMessage(0) # 退出消息监听
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    # 注册窗口类
    def create_hidden_window(self):
        wnd_class = win32gui.WNDCLASS()
        wnd_class.lpfnWndProc = {
            win32con.WM_QUERYENDSESSION: self.wnd_proc,
            win32con.WM_ENDSESSION: self.wnd_proc
        }
        wnd_class.lpszClassName = "ShutdownListener"
        wnd_class.hInstance = win32api.GetModuleHandle(None)
        hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_LEFT, # 扩展窗口样式，WS_EX_LEFT表示左对齐，通常设置为0
            win32gui.RegisterClass(wnd_class), # 注册窗口类并返回类原子标识符
            "ShutdownListener",  # 窗口标题
            0,  # 窗口样式
            0, 0,  # 窗口位置 (x, y)
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, # 窗口尺寸 (width, height)
            0,  # 父窗口句柄，0表示没有父窗口
            0,  # 菜单句柄，0表示没有菜单
            wnd_class.hInstance,  # 实例句柄
            None  # 额外的参数，通常为 None
        )
        self.hwnd = hwnd

    def destroy_hidden_window(self):
        if self.hwnd is not None:
            win32gui.DestroyWindow(hwnd)
            win32gui.UnregisterClass("ShutdownListener", win32api.GetModuleHandle(None))

    def run(self):
        print("ShutdownListener run")
        logging.info("ShutdownListener run")
        self.create_hidden_window()
        win32gui.PumpMessages()  # 启动消息监听
        print("ShutdownListener quit")
        logging.info("ShutdownListener quit")
        self.destroy_hidden_window()

shutdownListener = ShutdownListener()
