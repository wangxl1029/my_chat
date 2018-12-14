import queue
import collections
import threading
import time
import os
import random
import functools


def random_bool():
    return random.random() < 0.5


def repored(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        print(f'{function.__name__} is reported.')
    return wrapper


class AliveThread(threading.Thread):
    @classmethod
    def create(cls, start_flag=True):
        # print(f'the class name is {cls}')
        t = cls()
        t.daemon = True
        if start_flag:
            t.start()
        return t


class FilesystemSensor(AliveThread):
    # @staticmethod
    # def create(start_flag=True):
    #     t = FilesystemSensor()
    #     t.daemon = True
    #     if start_flag:
    #         t.start()
    #     return t

    def __init__(self):
        super().__init__()
        self.__step_reset_target()
        self.iq = queue.Queue()
        self.oq = queue.Queue()

    def __del__(self):
        self.iq.task_done()
        self.oq.task_done()
        self.iq.join()
        self.oq.join()

    def __next_step(self):
        if self.__ctx_target is None:
            self.__step_reset_target()
        elif os.path.isdir(self.__ctx_target):
            self.__step_walk_dir()
        elif os.path.isfile(self.__ctx_target):
            self.__step_walk_file_property()
        else:
            self.__step_reset_target()

    @repored
    def __step_reset_target(self):
        self.__ctx_target = os.getcwd()

    def __walking_fullname(self, cur_dir):
        for root, dirs, files in os.walk(cur_dir):
            for filename in files:
                fullname = os.path.join(root, filename)
                yield fullname

    @repored
    def __step_walk_dir(self):
        for fullname in self.__walking_fullname(self.__ctx_target):
            print(f'walk dir@{fullname}')

        self.__ctx_target = None

    def deprecated__step_walk_dir(self):
        is_broken = False
        cur_dir = self.__ctx_target
        for root, dirs, files in os.walk(cur_dir):
            for filename in files:
                fullname = os.path.join(root, filename)
                self.__ctx_target = fullname
                print(f'walk dir @ {self.__ctx_target}')

                is_broken = random_bool()
                if is_broken:
                    break

            if is_broken:
                break

        if not is_broken:
            self.__ctx_target = None

    def __step_walk_file_property(self):
        cur_file = self.__ctx_target
        print(f'walk file property @ {self.__ctx_target}')
        self.__ctx_target = None

    # override the method of supper class
    def run(self):
        while True:
            time.sleep(1)
            print('fs awake!')
            self.__next_step()

    def __example_codes(self):
        date_from_name = {}
        dir_list = []
        for name in os.listdir(self.__ctx_target):
            fullname = os.path.join(self.__ctx_target, name)
            if os.path.isfile(fullname):
                date_from_name[fullname] = os.path.getatime(fullname)
                print(f'{fullname}, {date_from_name[fullname]}')
            elif os.path.isdir(fullname):
                dir_list += [fullname]

    def __example_codes_2(self):
        data = collections.defaultdict(list)

        for root, dirs, files in os.walk(self.__ctx_target):
            for filename in files:
                fullname = os.path.join(root, filename)
                key = (os.path.getsize(fullname), filename)
                data[key].append(fullname)


g_fs_sensor = FilesystemSensor.create()


class AliveMessager(AliveThread):
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
