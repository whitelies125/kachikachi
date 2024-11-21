from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import time
import logging

def create_image():
    """生成一个简单的图标图片"""
    width = 64
    height = 64
    color1 = "blue"
    color2 = "white"

    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)
    draw.ellipse((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=color2)
    return image

def on_stop(icon, item, stop_event, exit_event):
    print(f"item : {item}")
    stop_event.set()
    icon.menu = Menu(
        MenuItem(f"Status: Stopping", None),
        MenuItem("Continue record", lambda icon, item: on_continue(icon, item, stop_event, exit_event)),
        MenuItem("Exit", lambda icon, item: on_exit(icon, item, exit_event))
    )

def on_continue(icon, item, stop_event, exit_event):
    print(f"item : {item}")
    stop_event.clear()
    icon.menu = Menu(
        MenuItem(f"Status: Recording", None),
        MenuItem("Stop record", lambda icon, item: on_stop(icon, item, stop_event, exit_event)),
        MenuItem("Exit", lambda icon, item: on_exit(icon, item, exit_event))
    )

def on_exit(icon, item, exit_event):
    print(f"item : {item}")
    exit_event.set()
    icon.stop()

def background_task(stop_event, exit_event):
    while not exit_event.is_set():
        print(f"exit: {exit_event.is_set()}, stop: {stop_event.is_set()}")
        logging.info(f"exit: {exit_event.is_set()}, stop: {stop_event.is_set()}")
        if stop_event.is_set():
            print("task stop...")
            logging.info("task stop...")
            time.sleep(1)
            continue
        print("task running...")
        logging.info("task running...")
        time.sleep(1)
    print("task exit")
    logging.info("task exit")

def main():
    logging.basicConfig(
        filename="background_log.txt",  # 日志文件名
        level=logging.INFO,  # 设置最低记录级别
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w",  # 写入模式：'w' 覆盖，'a' 追加
    )

    stop_event = threading.Event()
    exit_event = threading.Event()
    # 启动后台线程
    # deamen = False, 主线程等待子线程退出后才退出
    threading.Thread(target = background_task, args = (stop_event, exit_event), daemon = False).start()

    # 创建菜单
    menu = Menu(
        MenuItem(f"Status: Recording", None),
        MenuItem("Stop record", lambda icon, item: on_stop(icon, item, stop_event, exit_event)),
        MenuItem("Exit", lambda icon, item: on_exit(icon, item, exit_event))
    )
    # 创建托盘图标
    icon = Icon("kachikachi", create_image(), "Kachikachi", menu=menu)
    # 运行托盘图标
    icon.run()

if __name__ == "__main__":
    main()
