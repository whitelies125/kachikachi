import sqlite3
import logging

class DbManager:
    def __init__(self):
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
        self.conn = conn
        self.cursor = cursor

    def __del__(self):
        print("dbManager delete")
        logging.info("dbManager delete")
        self.conn.commit()
        self.conn.close()

    def get_process_tbl(self):
        self.cursor.execute("SELECT * FROM process")
        rows = self.cursor.fetchall()
        process_tbl = { k: v for v, k in rows }
        return process_tbl

    def insert_process_tbl(self, process):
        self.cursor.execute("INSERT INTO process (process) VALUES (?)", (process,))

    def insert_activity_tbl(self, activity_item):
        # 插入语句
        insert_sql = "INSERT INTO activity (process_id, start_time, end_time) VALUES (?, ?, ?)"
        # 待插入数据
        data = (activity_item.process_id, activity_item.start_time, activity_item.end_time)
        # 执行插入操作
        self.cursor.execute(insert_sql, data)

    def commit(self):
        print("dbManager commit")
        logging.info("dbManager commit")
        self.conn.commit()
