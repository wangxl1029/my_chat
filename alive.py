import queue
import threading


class BackgroundAliveThread(threading.Thread):
    @staticmethod
    def create():
        t = BackgroundAliveThread()
        t.daemon = True
        t.start()
        return t

    def __init__(self):
        super().__init__()
        self.iq = queue.Queue()
        self.oq = queue.Queue()

    def __del__(self):
        self.iq.task_done()
        self.oq.task_done()
        self.iq.join()
        self.oq.join()

    def run(self):
        count = 0
        while True:
            count += 1
            msg: str = self.iq.get()
            self.oq.put(f'#{count} : feedback message \"{msg}\".\n')

    def send_msg(self, msg):
        self.iq.put(msg)

    def get_msg(self):
        return self.oq.get()