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

def main():
    print("Start tracking active window. Press Ctrl+C to stop.")
    record_dict = dict()
    title, process_name = get_active_window_title_and_process_name()
    if title != "":
        record_dict[process_name] = 0
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    # 时间戳
    pre_time = int(time.time())
    try:
        while True:
            title, process_name = get_active_window_title_and_process_name()
            if title != "":
                now = datetime.now()
                year, month, day = now.year, now.month, now.day
                cur_time = int(time.time())
                duration = cur_time - pre_time
                pre_time = cur_time
                # print(f"Year: {year}, Month: {month}, Day: {day}, Timestamp: {pre_time}, duration: {duration}")
                # 若key存在，则返回value；若不存在则则返回 0
                record_dict[process_name] = record_dict.get(process_name, 0) + duration
            print(record_dict)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped tracking active window.")

if __name__ == "__main__":
    main()
