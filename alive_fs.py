import os
import collections
from alive_mem import *
from alive_util import *
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


class FilesystemSensor(AliveThread):
    def __init__(self):
        super().__init__()
        self.__step_reset_target()
        self.__qp = QueuePipe()

    def __del__(self):
        self.__qp.task_done()
        self.__qp.join()

    @reported
    def __step_check_prop(self):
        target = self.__ctx_target
        prop = None

        if target is not None:
            target_type = FsTargetEnum.regular_file if os.path.isfile(target) else \
                FsTargetEnum.directory if os.path.isdir(target) else FsTargetEnum.unknown

            prop = target, target_type

        feedback = MemoryInfoEnum.fs_target_prop_done, prop
        g_mem.put(feedback)

    @reported
    def __step_walk_directory(self):
        data = None
        if self.__ctx_target is None:
            pass

        feedback = MemoryInfoEnum.fs_target_list_done, data
        g_mem.put(feedback)

    @reported
    def __step_list_target(self):
        data = None
        if self.__ctx_target is None:
            pass

        feedback = MemoryInfoEnum.fs_target_list_done, data
        g_mem.put(feedback)

    @reported
    def __step_reset_target(self):
        self.__ctx_target = os.getcwd()
        feedback = MemoryInfoEnum.fs_target_reset_done, self.__ctx_target
        g_mem.put(feedback)

    @staticmethod
    def __walking_fullname(cur_dir):
        for root, dirs, files in os.walk(cur_dir):
            for filename in files:
                fullname = os.path.join(root, filename)
                yield fullname

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

    # override the method of supper class
    def run(self):
        action = {
            FsCommandEnum.reset: self.__step_reset_target,
            FsCommandEnum.list_dir: self.__step_list_target,
            FsCommandEnum.get_prop: self.__step_check_prop,
            FsCommandEnum.walk: self.__step_walk_directory
        }
        while True:
            cmd = self.__qp.inner_get()
            action[cmd]()
            print(f'{cmd}')

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
