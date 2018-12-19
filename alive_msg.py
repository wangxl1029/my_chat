import alive_mem as am
import alive_util as au
import util_channel as channel


class UniqueIdGenerator:
    pass


class AliveMessager(au.AliveThread):
    def __init__(self):
        # assert isinstance(queue, chan_mem2me)
        super().__init__()
        self.__chan_from_mem = channel.mem2messager
        self.__chan_from_user = channel.user2messager

    def __del__(self):
        self.__qp.join()

    # override the super class method
    def run(self):
        count = 0
        while True:
            count += 1
            try:
                msg = self.__chan_from_user.get()

                am.instance().put((am.MemoryInfoEnum.msg_input, msg))
            finally:
                self.__chan_from_user.task_done()

    def send_msg(self, msg):
        self.__chan_from_user.put(msg)
        print(f'messager send : \"{msg}\"')

    def get_msg(self):
        return self.__chan_from_mem.get()


_alive_messager = AliveMessager.create()


def instance():
    return _alive_messager
