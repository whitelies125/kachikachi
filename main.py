import logging
import threading

from kachikachi import kachikachi
from shutdown_listener import ShutdownListener
from tray import Tray

def listen_for_shutdown(icon, exit_event):
    shutdownListener = ShutdownListener(icon, [exit_event])
    shutdownListener.run()

class ThreadManager:
    def __init__(self):
        self.threads = []

    def start_thread(self, target, args=(), daemon=False):
        # deamen = False, 非守护线程，主线程退出时等待子线程退出后才退出
        # deamen = True, 守护线程，主线程退出时强制终止子线程
        thread = threading.Thread(target = target, args = args, daemon = daemon)
        thread.start()
        self.threads.append(thread)

    def join_all(self):
        for thread in self.threads:
            if not thread.daemon:
                thread.join()

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

    # 创建菜单
    tray = Tray(record_event, exit_event)

    thread_manager = ThreadManager()
    thread_manager.start_thread(kachikachi, args=(record_event, exit_event), daemon=False)
    thread_manager.start_thread(listen_for_shutdown, args=(tray.icon, exit_event), daemon=True)

    # 运行托盘程序
    tray.run()
    # 在主程序退出时，确保所有非守护线程完成工作
    thread_manager.join_all()

if __name__ == "__main__":
    main()
