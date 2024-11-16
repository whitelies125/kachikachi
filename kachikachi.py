import time
import win32gui
import win32process
import psutil

from datetime import datetime

def get_active_window_title_and_process_name():
    hwnd = win32gui.GetForegroundWindow()  # 获取当前激活窗口的句柄
    if not hwnd:
        return "", ""
    # 当前激活窗口的标题
    window_title = win32gui.GetWindowText(hwnd)  # 获取窗口标题
    _, pid = win32process.GetWindowThreadProcessId(hwnd)  # 获取窗口所属的进程 ID
    process = psutil.Process(pid)  # 获取进程对象
    # 当前激活窗口的进程名
    process_name = process.name()  # 返回进程名称
    return window_title, process_name

class Activity_item:
    # 起止时间，左闭右开
    def __init__(self, process, start_time):
        self.process = process
        self.start_time = start_time
        self.end_time = start_time

    def __str__(self):
        return f"{self.process}, {self.start_time}, {self.end_time}"

def main():
    process_dict = dict()
    activity = list()
    title, process = "", ""
    while True:
        title, process = get_active_window_title_and_process_name()
        print(f"tile : {title}, process {process}")
        if title != "":
            break;
        time.sleep(1)
    activity_item = Activity_item(process, int(time.time()))
    index = 1
    while True:
        cur_time = int(time.time())
        title, process = get_active_window_title_and_process_name()
        if title != "":
            activity_item.end_time = cur_time;
            if process != activity_item.process:
                activity.append(activity_item)
                activity_item = Activity_item(process, cur_time)
            [print(x) for x in activity]
            # 若key存在，则返回value；若不存在则则返回 0
            if process not in process_dict:
                process_dict[process] = index;
                index += 1
        print(process_dict)
        time.sleep(1)

if __name__ == "__main__":
    main()
