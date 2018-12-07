import queue
import threading


class MessageMemory(threading.Thread):
    def __init__(self):
        super().__init__()
        self.mq = queue.Queue()
        self.max_msg_num = 3

    def __del__(self):
        self.mq.task_done()
        self.mq.join()

    def run(self):
        msg_num_max = 3
        msg_list = []
        while True:
            msg = self.mq.get()
            msg_list.append(msg)
            if len(msg_list) > msg_num_max:
                m = msg_list.pop()
                print(f'remove msg "{m}"')

    def push(self, msg):
        self.mq.put(msg)
