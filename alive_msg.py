import alive_mem as am
import alive_util as au
import util_channel as channel


class UniqueIdGenerator:
    pass


class AliveMessager(au.AliveThread):
    def __init__(self):
        # assert isinstance(queue, chan_mem2me)
        super().__init__()
        self.__qp = au.QueuePipe()
        self.__chan_from_mem = channel.mem2messager

    def __del__(self):
        self.__qp.join()

    # override the super class method
    def run(self):
        count = 0
        while True:
            count += 1
            msg = None
            try:
                msg = self.__qp.inner_get()

                am.instance().put((am.MemoryInfoEnum.msg_input, msg))
            finally:
                # self.__qp.task_done()
                print("task done")

    def send_msg(self, msg):
        self.__qp.outer_put(msg)
        print(f'messager send : \"{msg}\"')

    def get_msg(self):
        self.__qp.inner_put(am.instance().get())
        return self.__qp.outer_get()


_alive_messager = AliveMessager.create()


def instance():
    return _alive_messager
