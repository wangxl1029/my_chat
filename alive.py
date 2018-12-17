import queue
import collections
import threading
# import time
import os
import random
import functools
from enum import Enum, unique


@unique
class FsTargetEnum(Enum):
    unknown = 0
    regular_file = 1
    directory = 2


@unique
class FsCommandEnum(Enum):
    reset = 0
    get_prop = 2
    list_dir = 3
    walk = 4


def repored(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        print(f'{function.__name__} is reported.')
    return wrapper


class UniqueIdGenerator:
    pass


class AliveThread(threading.Thread):
    @classmethod
    def create(cls, start_flag=True):
        t = cls()
        t.daemon = True
        if start_flag:
            t.start()
        return t


class QueuePipe:
    def __init__(self):
        self.__iq = queue.Queue()
        self.__oq = queue.Queue()

    def inner_get(self, block=True, timeout=None):
        return self.__iq.get(block, timeout)

    def inner_put(self, item):
        self.__oq.put(item)

    def outer_get(self):
        return self.__oq.get()

    def outer_put(self, item):
        self.__iq.put(item)

    def task_done(self):
        self.__iq.task_done()
        self.__oq.task_done()

    def join(self):
        self.__iq.join()
        self.__oq.join()


class AliveMemory(AliveThread):
    def __init__(self):
        super().__init__()
        self.__qp = QueuePipe()

    def __del__(self):
        self.__qp.task_done()
        self.__qp.join()

    # override the method of supper class
    def run(self):
        while True:
            try:
                msg = self.__qp.inner_get(True, 1)
                self.__qp.inner_put(msg)
                print('memory alive!')
            except queue.Empty:
                print('memory timeout')

            cmd = random.choice([FsCommandEnum.reset, FsCommandEnum.get_prop,
                                 FsCommandEnum.list_dir, FsCommandEnum.walk])
            g_fs_sensor.send_cmd(cmd)

    def put(self, item):
        self.__qp.outer_put(item)

    def get(self):
        return self.__qp.outer_get()


g_mem = AliveMemory.create()


class FilesystemSensor(AliveThread):
    def __init__(self):
        super().__init__()
        self.__step_reset_target()
        self.__qp = QueuePipe()

    def __del__(self):
        self.__qp.task_done()
        self.__qp.join()

    def __next_step(self):
        if self.__ctx_target is None:
            self.__step_reset_target()
        elif os.path.isdir(self.__ctx_target):
            self.__step_walk_dir()
        elif os.path.isfile(self.__ctx_target):
            self.__step_walk_file_property()
        else:
            self.__step_reset_target()

    def __step_check_prop(self):
        target = self.__ctx_target
        # region Description
        if target is not None:
            target_type = FsTargetEnum.regular_file if os.path.isfile(target) else \
                FsTargetEnum.directory if os.path.isdir(target) else FsTargetEnum.unknown
            prop = target, target_type
            g_mem.put(prop)
            target_list = None
            ctx = prop, target_list
            return ctx
        # endregion

    @repored
    def __update_context(self):
        pass

    def __step_make_target_list(self):
        pass

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
            # print(f'walk dir@{fullname}')
            g_mem.put(fullname)

        self.__ctx_target = None

    def deprecated__step_walk_dir(self):
        is_broken = False
        cur_dir = self.__ctx_target
        for root, dirs, files in os.walk(cur_dir):
            for filename in files:
                fullname = os.path.join(root, filename)
                self.__ctx_target = fullname
                print(f'walk dir @ {self.__ctx_target}')

                is_broken = random.choice([True, False])
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
        action = {
            FsCommandEnum.reset: self.__step_reset_target,
            FsCommandEnum.list_dir: self.__step_make_target_list,
            FsCommandEnum.get_prop: self.__step_check_prop,
            FsCommandEnum.walk: self.__step_walk_file_property
        }
        ctx = None
        count: int = 0
        while True:
            count += 1
            # time.sleep(1)
            # print(f'file system awake #{count}')
            cmd = self.__qp.inner_get()
            action[cmd]()
            print(f'{cmd}')
            # self.__next_step()
            # self.__update_context()
            # self.__instinct(ctx)

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

    def send_cmd(self, cmd):
        self.__qp.outer_put(cmd)


g_fs_sensor = FilesystemSensor.create()


class AliveMessager(AliveThread):
    def __init__(self):
        super().__init__()
        self.__qp = QueuePipe()

    def __del__(self):
        self.__qp.join()

    # override the super class method
    def run(self):
        count = 0
        while True:
            count += 1
            try:
                msg = self.__qp.inner_get()
                # self.__qp.inner_put(f'#{count} got message \"{msg}\".')
                g_mem.put(msg)

            finally:
                self.__qp.task_done()

    def send_msg(self, msg):
        self.__qp.outer_put(msg)
        print(f'messager send : \"{msg}\"')

    def get_msg(self):
        self.__qp.inner_put(g_mem.get())
        return self.__qp.outer_get()
