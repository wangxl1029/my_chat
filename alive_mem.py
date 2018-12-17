import random

from alive_fs import *
from alive_util import *


@unique
class MemoryInfoEnum(Enum):
    fs_target_reset_done = 0
    fs_target_prop_done = 1
    fs_target_list_done = 2
    fs_target_walk_done = 3

    msg_input = 10


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
                info_type, info_data = self.__qp.inner_get(True, 1)
                if info_type == MemoryInfoEnum.msg_input:
                    self.__qp.inner_put(info_data)
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
