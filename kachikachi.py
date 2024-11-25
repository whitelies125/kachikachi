import time
import win32gui
import win32process
import psutil
import logging

from db_manager import DbManager
from thread_manager import threadManager

def get_active_window_title_and_process_name():
    hwnd = win32gui.GetForegroundWindow()  # 获取当前激活窗口的句柄
    # 熄屏后会没有 hwnd
    if not hwnd:
        return None, None
    # 当前激活窗口的标题
    window_title = win32gui.GetWindowText(hwnd)  # 获取窗口标题
    _, pid = win32process.GetWindowThreadProcessId(hwnd)  # 获取窗口所属的进程 ID
    process = psutil.Process(pid)  # 获取进程对象
    # 当前激活窗口的进程名
    process_name = process.name()  # 返回进程名称
    return window_title, process_name

class Activity_item:
    # 起止时间，左闭右开
    def __init__(self, process_id, start_time):
        self.process_id = process_id
        self.start_time = start_time
        self.end_time = start_time

    def __str__(self):
        return f"{self.process_id}, {self.start_time}, {self.end_time}"

def kachikachi():
    dbManager = DbManager()
    activity_item = None;
    process_tbl = { v: k for k, v in dbManager.get_process_tbl() }
    while not threadManager.exit_event.is_set():
        if not threadManager.record_event.is_set():
            threadManager.record_event.wait(1)
            continue;
        if threadManager.plot_event.is_set():
            dbManager.commit()
            threadManager.plot_event.clear()

        cur_time = int(time.time())
        title, process = get_active_window_title_and_process_name()
        logging.info(f"kachikachi, {title}, {process}")
        if process == None:
            if activity_item == None:
                print("kachikachi None None...")
                logging.warn("kachikachi, None None...")
                threadManager.exit_event.wait(60)
                continue;
            if activity_item != None:
                activity_item.end_time = cur_time;
                logging.info(f"kachikachi, insert process to null {activity_item}")
                dbManager.insert_activity_tbl(activity_item)
                activity_item = None
        if process != None:
            if process not in process_tbl:
                dbManager.insert_process_tbl(process)
                process_tbl = { v: k for k, v in dbManager.get_process_tbl() }
            if activity_item == None:
                activity_item = Activity_item(process_tbl[process], cur_time)
            activity_item.end_time = cur_time;
            if process_tbl[process] != activity_item.process_id:
                logging.info(f"kachikachi, insert process change {activity_item}")
                dbManager.insert_activity_tbl(activity_item)
                activity_item = Activity_item(process_tbl[process], cur_time)

        print("kachikachi task running...")
        logging.info("kachikachi, task running...")
        threadManager.exit_event.wait(60)

    if activity_item != None:
        logging.info(f"kachikachi, insert thread exit {activity_item}")
        dbManager.insert_activity_tbl(activity_item)
    dbManager.disconnect()
    print("kachikachi, thread exit")
    logging.info("kachikachi, thread exit")
