import threading

class ThreadManager:
    def __init__(self):
        self.threads = []
        self.record_event = threading.Event()
        self.exit_event = threading.Event()
        self.plot_event = threading.Event()

        self.record_event.set()

    def start_thread(self, target, args=(), daemon=False):
        # deamen = False, 非守护线程，主线程退出时等待子线程退出后才退出
        # deamen = True, 守护线程，主线程退出时强制终止子线程
        thread = threading.Thread(target = target, args = args, daemon = daemon)
        thread.start()
        self.threads.append(thread)

    # 在主程序退出时，确保所有非守护线程完成工作
    def join_all(self):
        for thread in self.threads:
            if not thread.daemon:
                thread.join()

threadManager = ThreadManager()
