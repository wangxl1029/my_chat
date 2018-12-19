import os
import collections
import random
from enum import Enum, unique
import alive_util
import util_channel as channel
import alive_mem as am


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


class FilesystemSensor(alive_util.AliveThread):
    def __init__(self):
        super().__init__()
        self.__ctx_target = None
        self.__chan_from_mem = channel.mem2fs
        self.__chan_to_mem = channel.any2mem

    def __del__(self):
        self.__chan_from_mem.join()

    @alive_util.reported
    def __step_check_prop(self):
        target = self.__ctx_target
        prop = None

        if target is not None:
            target_type = FsTargetEnum.regular_file if os.path.isfile(target) else \
                FsTargetEnum.directory if os.path.isdir(target) else FsTargetEnum.unknown

            prop = target, target_type

        feedback = am.MemoryInfoEnum.fs_target_prop_done, prop
        self.__chan_to_mem.put(feedback)

    @alive_util.reported
    def __step_walk_directory(self):
        data = None
        if self.__ctx_target is None:
            pass

        feedback = am.MemoryInfoEnum.fs_target_list_done, data
        self.__chan_to_mem.put(feedback)

    @alive_util.reported
    def __step_list_target(self):
        data = None
        if self.__ctx_target is None:
            pass

        feedback = am.MemoryInfoEnum.fs_target_list_done, data
        self.__chan_to_mem.put(feedback)

    @alive_util.reported
    def __step_reset_target(self):
        self.__ctx_target = os.getcwd()
        feedback = am.MemoryInfoEnum.fs_target_reset_done, self.__ctx_target
        self.__chan_to_mem.put(feedback)

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
            try:
                cmd = self.__chan_from_mem.get()
            finally:
                self.__chan_from_mem.task_done()
                action[cmd]()
                # print(f'{cmd}')

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


_fs_sensor = FilesystemSensor.create()


def instance():
    return _fs_sensor
