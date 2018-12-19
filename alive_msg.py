import alive_mem as am
import alive_util as au
import util_channel as channel


class UniqueIdGenerator:
    pass


class AliveMessager(au.AliveThread):
    def __init__(self):
        super().__init__()
        self.__chan_from_mem = channel.mem2messager
        self.__chan_from_user = channel.user2messager
        self.__chan_to_mem = channel.any2mem

    def __del__(self):
        self.__chan_from_user.join()

    # override the super class method
    def run(self):
        while True:
            try:
                msg = self.__chan_from_user.get()

            finally:
                self.__chan_from_user.task_done()
                self.__chan_to_mem.put((am.MemoryInfoEnum.msg_input, msg))

    def send_msg(self, msg):
        self.__chan_from_user.put(msg)

    def get_msg(self):
        return self.__chan_from_mem.get()


_alive_messager = AliveMessager.create()


def instance():
    return _alive_messager
