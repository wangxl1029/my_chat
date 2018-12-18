import functools
import queue
import threading


def reported(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        # print(f'{function.__name__} is reported.')
    return wrapper


class AliveThread(threading.Thread):
    @classmethod
    def create(cls, start_flag=True):
        print(f'thread {cls} to be created.')
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
