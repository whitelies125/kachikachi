import os
import logging
import threading

from kachikachi import kachikachi
from shutdown_listener import shutdownListener
from tray import trayInst
from thread_manager import threadManager

def callback():
    threadManager.exit_event.set()
    trayInst.icon.stop()

def listen_for_shutdown():
    shutdownListener.addCallback(callback)
    shutdownListener.run()

def main():
    path  = os.path.dirname(__file__)
    os.chdir(path)
    logging.basicConfig(
        filename = "log.txt",  # 日志文件名
        level = logging.INFO,  # 设置最低记录级别
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        filemode = "w",  # 写入模式：'w' 覆盖，'a' 追加
    )
    print("pwd: ", os.getcwd())
    logging.info(f"pwd, {os.getcwd()}")

    threadManager.start_thread(kachikachi, daemon=False)
    threadManager.start_thread(listen_for_shutdown, daemon=True)

    # 运行托盘程序
    trayInst.run()
    threadManager.join_all()
    print("process quit")
    logging.info("process quit")

if __name__ == "__main__":
    main()
