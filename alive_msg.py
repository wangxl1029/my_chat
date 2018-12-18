import alive_mem as am
import alive_util as au


class UniqueIdGenerator:
    pass


class AliveMessager(au.AliveThread):
    def __init__(self):
        super().__init__()
        self.__qp = au.QueuePipe()

    def __del__(self):
        self.__qp.join()

    # override the super class method
    def run(self):
        count = 0
        while True:
            count += 1
            try:
                msg = self.__qp.inner_get()
                am.instance().put((am.MemoryInfoEnum.msg_input, msg))

            finally:
                self.__qp.task_done()

    def send_msg(self, msg):
        self.__qp.outer_put(msg)
        print(f'messager send : \"{msg}\"')

    def get_msg(self):
        self.__qp.inner_put(am.instance().get())
        return self.__qp.outer_get()
