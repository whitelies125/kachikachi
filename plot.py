import argparse
from datetime import datetime
import matplotlib.pyplot as plt

import json
from db_manager import DbManager

def custom_autopct(pct):
    return f'{pct:.2f}%' if pct >= 1 else ''

def get_group_name(group, process_name):
    for key, value in group.items() :
        if process_name in value:
            return key
    return process_name

def load_config():
    ignore = list()
    group = dict()
    config = "./config.json"
    try:
        with open(config, "r", encoding="utf-8") as file:
            data = json.load(file)
            if 'ignore' in data:
                ignore = data['ignore']
            if 'group' in data:
                group = data['group']
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print(f"{config} JSON decode fail.")
    return ignore, group

def arg_config(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-today", action = "store_true", help = "Plot today data.")
    group.add_argument("-seven_day", action = "store_true", help = "Plot recently senven day data.")
    group.add_argument("-month", action = "store_true", help = "Plot this month data.")
    group.add_argument("-year", action = "store_true", help = "Plot this year data.")
    group.add_argument("-all", action = "store_true", help = "Plot all data.")
    parser.add_argument("-start_time", type=int, help="Start time in timestamp format.")
    parser.add_argument("-end_time", type=int, help="End time in timestamp format.")

def get_query_time(parser):
    args = parser.parse_args()
    query_start_time = None
    query_end_time = None
    now = datetime.now()
    if args.today:
        query_start_time = int(datetime(now.year, now.month, now.day).timestamp())
    elif args.seven_day:
        query_start_time = int(datetime(now.year, now.month, now.day).timestamp()) - 6 * 24 * 60 * 60
    elif args.month:
        query_start_time = int(datetime(now.year, now.month, 1).timestamp())
    elif args.year:
        query_start_time = int(datetime(now.year, 1, 1).timestamp())

    if args.start_time:
        query_start_time = args.start_time
    if args.end_time:
        query_end_time = args.end_time

    return query_start_time, query_end_time

def plot():
    parser = argparse.ArgumentParser(description="Plot database data.")
    arg_config(parser)
    query_start_time, query_end_time = get_query_time(parser)
    ignore, group = load_config()

    dbManager = DbManager()
    process_tbl = { k: v for k, v in dbManager.get_process_tbl() }
    activity_tbl = dbManager.get_activity_tbl(query_start_time, query_end_time)
    dbManager.disconnect()

    statistic = dict()
    total = 0
    for activity in activity_tbl :
        index, process_id, start_time, end_time = activity
        if query_start_time and start_time < query_start_time:
            start_time = query_start_time
        if query_end_time and end_time > query_end_time:
            end_time = query_end_time
        duration = end_time - start_time
        process_name = process_tbl[process_id]
        if process_name not in ignore:
            group_name = get_group_name(group, process_name)
            statistic[group_name] = statistic.get(group_name, 0) + duration
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
