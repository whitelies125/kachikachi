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

def custom_autopct(pct):
    return f'{pct:.2f}%' if pct >= 1 else ''

def plot():
    conn, cursor = db_init()
    process_tbl = get_process_tbl(cursor)
    activity_tbl = get_activity_tbl(cursor)
    conn.close()
    statistic = dict()
    total = 0
    for activity in activity_tbl :
        index, process_id, start_time, end_time = activity
        duration = end_time - start_time
        statistic[process_tbl[process_id]] = statistic.get(process_tbl[process_id], 0) + duration
        total += duration
    for process in statistic:
        statistic[process] = statistic[process] / total * 100
    statistic = sorted(statistic.items(), key = lambda item: item[1], reverse = True)

    color = ['#F27970', '#F49821', '#D5F566', '#E2CE6E', '#9E6BD4', '#68A76A', '#54A7CC']
    # 小于 1% 的数据仅显示色块
    labels = [item[0] if item[1] >= 1 else '' for item in statistic]
    sizes = [item[1] for item in statistic]
    # 绘制饼图
    plt.pie(sizes,
            labels = labels,
            autopct = custom_autopct,
            colors = color
            )
    # 显示图表
    plt.title('statistic')
    plt.show()

def main():
    plot()

if __name__ == "__main__":
    main()
