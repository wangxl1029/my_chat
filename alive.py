import queue
import threading
import time


class FilesystemSensor(threading.Thread):
    @staticmethod
    def create(start_flag=True):
        t = FilesystemSensor()
        t.daemon = True
        if start_flag:
            t.start()
        return t

    def __init__(self):
        super().__init__()
        self.iq = queue.Queue()
        self.oq = queue.Queue()

    def __del__(self):
        self.iq.task_done()
        self.oq.task_done()
        self.iq.join()
        self.oq.join()

    def run(self):
        while True:
            time.sleep(1)
            print('fs awake!')


g_fs_sensor = FilesystemSensor.create()


class AliveMessager(threading.Thread):
    @staticmethod
    def create(start_flag=True):
        t = AliveMessager()
        t.daemon = True
        if start_flag:
            t.start()
        return t

    def __init__(self):
        super().__init__()
        self.iq = queue.Queue()
        self.oq = queue.Queue()

    def __del__(self):
        self.iq.task_done()
        self.oq.task_done()
        self.iq.join()
        self.oq.join()

    def run(self):
        count = 0
        while True:
            count += 1
            msg: str = self.iq.get()
            self.oq.put(f'#{count} got message \"{msg}\".')

    def send_msg(self, msg):
        self.iq.put(msg)

    def get_msg(self):
        return self.oq.get()
