import queue
import threading
import time
import os


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
        self._reset_target()
        self.iq = queue.Queue()
        self.oq = queue.Queue()

    def __del__(self):
        self.iq.task_done()
        self.oq.task_done()
        self.iq.join()
        self.oq.join()

    def _reset_target(self):
        self.target_dir = os.getcwd()

    def run(self):
        while True:
            time.sleep(1)
            print('fs awake!')
            date_from_name = {}
            dir_list = []
            for name in os.listdir(self.target_dir):
                fullname = os.path.join(self.target_dir, name)
                if os.path.isfile(fullname):
                    date_from_name[fullname] = os.path.getatime(fullname)
                    print(f'{fullname}, {date_from_name[fullname]}')
                elif os.path.isdir(fullname):
                    dir_list += [fullname]

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
        self.__iq = queue.Queue()
        self.__oq = queue.Queue()

    def __del__(self):
        self.__iq.join()
        self.__oq.join()

    # override the super class method
    def run(self):
        count = 0
        while True:
            count += 1
            try:
                msg: str = self.__iq.get()
                self.__oq.put(f'#{count} got message \"{msg}\".')
            finally:
                self.__iq.task_done()
                self.__oq.task_done()

    def send_msg(self, msg):
        self.__iq.put(msg)

    def get_msg(self):
        return self.__oq.get()
