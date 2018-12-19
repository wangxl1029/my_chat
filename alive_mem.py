import random
import queue
from enum import Enum, unique

import alive_fs as fs
import alive_util as au
import util_channel as channel

__all__ = ["MemoryInfoEnum", "AliveMemory", "instance"]


@unique
class MemoryInfoEnum(Enum):
    none = 0

    fs_target_reset_done = 1
    fs_target_prop_done = 2
    fs_target_list_done = 3
    fs_target_walk_done = 4

    msg_input = 10


class AliveMemory(au.AliveThread):
    def __init__(self):
        super().__init__()
        self.__chan2me = channel.any2mem
        self.__chan2fs = channel.mem2fs
        self.__chan2messager = channel.mem2messager

    def __del__(self):
        self.__chan2me.task_done()
        self.__chan2me.join()

    # override the method of supper class
    def run(self):
        info_type = MemoryInfoEnum.none

        while True:
            try:
                info_type, info_data = self.__chan2me.get(True, 1)

            except queue.Empty:
                print('memory timeout')

            finally:

                if info_type == MemoryInfoEnum.msg_input:
                    self.__chan2messager.put(info_data)
                    print(f"-------> {info_data}")
                else:
                    # print(f'memory alive{info_type}!')
                    pass

            cmd = random.choice([fs.FsCommandEnum.reset, fs.FsCommandEnum.get_prop,
                                 fs.FsCommandEnum.list_dir, fs.FsCommandEnum.walk])

            self.__chan2fs.put(cmd)


_alive_mem = AliveMemory.create()


def instance():
    return _alive_mem
