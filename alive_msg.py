from enum import Enum, unique
from alive_util import *
from alive_mem import *


class UniqueIdGenerator:
    pass


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
