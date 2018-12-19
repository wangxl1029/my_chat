import random
from enum import Enum, unique

import alive_fs as fs
import alive_util as au
import util_channel as channel

__all__ = ["MemoryInfoEnum", "AliveMemory", "instance"]


@unique
class MemoryInfoEnum(Enum):
    fs_target_reset_done = 0
    fs_target_prop_done = 1
    fs_target_list_done = 2
    fs_target_walk_done = 3

    msg_input = 10


class AliveMemory(au.AliveThread):
    def __init__(self):
        super().__init__()
        self.__chan2messager = channel.mem2messager
        self.__qp = au.QueuePipe()

    def __del__(self):
        self.__qp.task_done()
        self.__qp.join()

    # override the method of supper class
    def run(self):
        while True:
            try:
                info_type, info_data = self.__qp.inner_get(True, 1)
                if info_type == MemoryInfoEnum.msg_input:
                    # self.__qp.inner_put(info_data)
                    self.__chan2messager.put(info_data)
                    print(f"-------> {info_data}")
                else:
                    # print(f'memory alive{info_type}!')
                    pass

            except au.queue.Empty:
                print('memory timeout')

            cmd = random.choice([fs.FsCommandEnum.reset, fs.FsCommandEnum.get_prop,
                                 fs.FsCommandEnum.list_dir, fs.FsCommandEnum.walk])
            fs.instance().send_cmd(cmd)

    def put(self, item):
        self.__qp.outer_put(item)

    def get(self):
        return self.__qp.outer_get()


_alive_mem = AliveMemory.create()


def instance():
    return _alive_mem
