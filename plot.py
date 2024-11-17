import sqlite3
import matplotlib.pyplot as plt

def db_init():
    database = "data.db"
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return conn, cursor

def get_process_tbl(cursor):
    cursor.execute("SELECT * FROM process")
    rows = cursor.fetchall()
    process_tbl = { k: v for k, v in rows }
    return process_tbl

def get_activity_tbl(cursor):
    cursor.execute("SELECT * FROM activity")
    rows = cursor.fetchall()
    return rows

# 自定义百分比格式化函数
def custom_autopct(pct):
    return f'{pct:.2f}%' if pct >= 2 else ''  # 仅显示 >= 2% 的数据

def main():
    conn, cursor = db_init()
    process_tbl = get_process_tbl(cursor)
    activity_tbl = get_activity_tbl(cursor)
    statistic = dict()
    total = 0
    for activity in activity_tbl :
        index, process_id, start_time, end_time = activity
        duration = end_time - start_time
        statistic[process_tbl[process_id]] = statistic.get(process_tbl[process_id], 0) + duration
        total += duration
    for process in statistic:
        statistic[process] = statistic[process] / total * 100

    # 绘制饼图
    plt.pie(statistic.values(),
            labels = statistic.keys(),
            autopct = custom_autopct,       # 显示格式为保留两位小数+%
            colors = plt.cm.tab20c.colors,  # 使用配色方案
            )
    # 显示图表
    plt.title('statistic')
    plt.show()
    conn.close()


if __name__ == "__main__":
    main()
