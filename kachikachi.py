import time
import win32gui
import win32process
import psutil
import sqlite3
import logging

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

def db_init():
    # 连接到 SQLite 数据库，若无则创建
    database = "data.db"
    conn = sqlite3.connect(database)
    # 创建游标对象
    cursor = conn.cursor()
    # 若无则创建表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS process (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 主键，自增
        process TEXT NOT NULL                  -- 进程名，非空
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 主键，自增
        process_id INTEGER NOT NULL,            -- 进程id，非空
        start_time INTEGER NOT NULL,            -- 开始时间，非空
        end_time INTEGER NOT NULL               -- 结束时间，非空
    )
    """)
    return conn, cursor

def get_process_tbl(cursor):
    cursor.execute("SELECT * FROM process")
    rows = cursor.fetchall()
    process_tbl = { k: v for v, k in rows }
    return process_tbl

def insert_process_tbl(cursor, process):
    cursor.execute("INSERT INTO process (process) VALUES (?)", (process,))

def insert_activity_tbl(cursor, activity_item):
    # 插入语句
    insert_sql = "INSERT INTO activity (process_id, start_time, end_time) VALUES (?, ?, ?)"
    # 待插入数据
    data = (activity_item.process_id, activity_item.start_time, activity_item.end_time)
    # 执行插入操作
    cursor.execute(insert_sql, data)

def main():
    logging.basicConfig(
        filename="kachikachi_log.txt",  # 日志文件名
        level=logging.INFO,  # 设置最低记录级别
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w",  # 写入模式：'w' 覆盖，'a' 追加
    )
    try:
        conn, cursor = db_init();
        process_tbl = get_process_tbl(cursor)

        activity_item = None;
        while True:
            cur_time = int(time.time())
            title, process = get_active_window_title_and_process_name()
            logging.info(f"{title}, {process}")
            if process == None:
                if activity_item == None:
                    time.sleep(60)
                if activity_item != None:
                    activity_item.end_time = cur_time;
                    logging.info(f"insert process to null {activity_item}")
                    insert_activity_tbl(cursor, activity_item)
                    activity_item = None
            if process != None:
                if process not in process_tbl:
                    insert_process_tbl(cursor, process)
                    process_tbl = get_process_tbl(cursor)
                if activity_item == None:
                    activity_item = Activity_item(process_tbl[process], cur_time)
                activity_item.end_time = cur_time;
                if process_tbl[process] != activity_item.process_id:
                    logging.info(f"insert process change {activity_item}")
                    insert_activity_tbl(cursor, activity_item)
                    activity_item = Activity_item(process_tbl[process], cur_time)
            time.sleep(60)
    except :
        if activity_item != None:
            logging.info(f"insert except {activity_item}")
            insert_activity_tbl(cursor, activity_item)
    if conn != None:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    main()

# export
def kachikachi(record_event, exit_event):
    conn, cursor = db_init()
    activity_item = None;
    while not exit_event.is_set():
        print(f"kachikachi, exit: {exit_event.is_set()}, record: {record_event.is_set()}")
        logging.info(f"kachikachi, exit: {exit_event.is_set()}, record: {record_event.is_set()}")
        record_event.wait()

        cur_time = int(time.time())
        process_tbl = get_process_tbl(cursor)
        title, process = get_active_window_title_and_process_name()
        logging.info(f"kachikachi, {title}, {process}")
        if process == None:
            if activity_item == None:
                time.sleep(10)
                continue;
            if activity_item != None:
                activity_item.end_time = cur_time;
                # logging.info(f"kachikachi, insert process to null {activity_item}")
                # insert_activity_tbl(cursor, activity_item)
                activity_item = None
        if process != None:
            if process not in process_tbl:
                insert_process_tbl(cursor, process)
                process_tbl = get_process_tbl(cursor)
            if activity_item == None:
                activity_item = Activity_item(process_tbl[process], cur_time)
            activity_item.end_time = cur_time;
            if process_tbl[process] != activity_item.process_id:
                # logging.info(f"kachikachi, insert process change {activity_item}")
                # insert_activity_tbl(cursor, activity_item)
                activity_item = Activity_item(process_tbl[process], cur_time)

        print("kachikachi task running...")
        logging.info("kachikachi, task running...")
        exit_event.wait(1)

    logging.info(f"kachikachi, break loop")
    if activity_item != None:
        logging.info(f"kachikachi, insert thread exit {activity_item}")
        insert_activity_tbl(cursor, activity_item)
    if conn != None:
        conn.commit()
        conn.close()
    print("kachikachi, thread exit")
    logging.info("kachikachi, thread exit")
