import csv
import argparse
from db_manager import DbManager
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Export database data.")
    parser.add_argument(
        "-origin",
        action = "store_true",
        help = "Export data as timestamps if specified, otherwise export as 'YYYY-MM-DD HH:MM:SS'."
    )
    args = parser.parse_args()

    dbManager = DbManager()
    process_tbl = dbManager.get_process_tbl()
    if process_tbl is None:
        return
    process_tbl = { v: k for k, v in process_tbl }
    activity_tbl = dbManager.get_activity_tbl()
    if activity_tbl is None:
        return
    dbManager.disconnect()

    data = list()
    for activity in activity_tbl:
        db_id, process_id, start_time, end_time = activity
        if not args.origin:
            start_time = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        data.append((db_id, process_tbl[process_id], start_time, end_time))
    print(data)

    with open('export.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'process_name', 'start_time', 'end_time'])
        for item in data:
            writer.writerow(item)

if __name__ == "__main__":
    main()
