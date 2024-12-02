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

def plot():
    ignore, group = load_config()

    dbManager = DbManager()
    process_tbl = { k: v for k, v in dbManager.get_process_tbl() }
    activity_tbl = dbManager.get_activity_tbl()
    dbManager.disconnect()

    statistic = dict()
    total = 0
    for activity in activity_tbl :
        index, process_id, start_time, end_time = activity
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
