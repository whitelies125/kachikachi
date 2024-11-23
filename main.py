import logging
import threading

from kachikachi import kachikachi
from shutdown_listener import ShutdownListener
from tray import Tray

def listen_for_shutdown(icon, exit_event):
    shutdownListener = ShutdownListener(icon, [exit_event])
    shutdownListener.run()

def main():
    logging.basicConfig(
        filename = "tray_log.txt",  # 日志文件名
        level = logging.INFO,  # 设置最低记录级别
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        filemode = "w",  # 写入模式：'w' 覆盖，'a' 追加
    )

    record_event = threading.Event()
    exit_event = threading.Event()
    record_event.set()
    # 启动后台线程
    # deamen = False, 主线程退出时等待子线程退出后才退出
    threading.Thread(target = kachikachi, args = (record_event, exit_event), daemon = False).start()

    # 创建菜单
    tray = Tray(record_event, exit_event)

    # 启动后台线程来监听关机事件
    # deamen = True, 主线程退出时强制终止子线程
    threading.Thread(target = listen_for_shutdown, args = (tray.icon, exit_event), daemon = True).start()

    # 运行托盘程序
    tray.run()

if __name__ == "__main__":
    main()
