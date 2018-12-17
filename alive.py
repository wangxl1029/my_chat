import queue
import collections
import threading
# import time
import os
import random
import functools
from enum import Enum, unique


@unique
class FsCommandEnum(Enum):
    reset = 0
    get_prop = 2
    list_dir = 3
    walk = 4


def reported(function):
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
                g_mem.put((MemoryInfoEnum.msg_input, msg))

            finally:
                self.__qp.task_done()

    def send_msg(self, msg):
        self.__qp.outer_put(msg)
        print(f'messager send : \"{msg}\"')

    def get_msg(self):
        self.__qp.inner_put(g_mem.get())
        return self.__qp.outer_get()
