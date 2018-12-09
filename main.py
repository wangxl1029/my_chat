import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QListWidget, QApplication, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QTextCursor

from alive import MessageMemory


class MessageActiveThread(QThread):
    sig_output = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        i = 1
        while True:
            self.sleep(1)
            self.sig_output.emit(f'#{i} some inner message\n')
            i = i + 1


class MessageWorker(QObject):
    work_done = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def do_work(self, msg):
        self.work_done.emit(f"{msg} done.\n")


class MessageController(QObject):
    operate = pyqtSignal(str)
    operate_done = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.worker_thread = QThread()
        self.worker = MessageWorker()
        self.worker.moveToThread(self.worker_thread)
        self.operate.connect(self.worker.do_work)
        self.worker.work_done.connect(self.operate_done)
        self.worker_thread.start()

    def __del__(self):
        self.worker_thread.quit()
        self.worker_thread.wait()


class MessageReceiver(QObject):
    def __init__(self):
        super().__init__()
        self.mem = MessageMemory()
        self.mem.daemon = True
        self.mem.start()

    def on_input(self, msg):
        print(msg)
        self.mem.push(msg)


class InputEdit(QTextEdit):
    sig_input = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

    def keyPressEvent(self, event):
        QTextEdit.keyPressEvent(self, event)
        key_code = event.key()
        if key_code == Qt.Key_Enter or key_code == Qt.Key_Return:
            # todo : to check shift key status
            self.sig_input.emit(self.toPlainText())
            self.setText("")


class OutputEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.message('welcome\n')

    def message(self, msg):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(msg)


class ChatUI(QWidget):

    def __init__(self):
        super().__init__()
        #self.msg_receiver = MessageReceiver()
        self.controller = MessageController()
        self.active_msg = MessageActiveThread(self)
        self.init_ui()

    def init_ui(self):
        h_box = QHBoxLayout(self)

        # the top left
        output_edit = OutputEdit(self)
        output_edit.setReadOnly(True)
        output_edit.setMinimumSize(400, 300)
        # the bottom left
        input_edit = InputEdit(self)
        input_edit.setMinimumHeight(50)
        input_edit.sig_input.connect(output_edit.message)
        #input_edit.sig_input.connect(self.msg_receiver.on_input)
        input_edit.sig_input.connect(self.controller.operate)
        # the right panel
        chat_list = QListWidget(self)

        # the splitter vertical
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(output_edit)
        splitter1.addWidget(input_edit)
        # the splitter horizontal
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(chat_list)

        # the layout overall
        h_box.addWidget(splitter2)
        self.setLayout(h_box)
        input_edit.setFocus()

        # the main window
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('My chat')
        self.show()

        # active/passive threads
        self.controller.operate_done.connect(output_edit.message)
        self.active_msg.sig_output.connect(output_edit.message)
        self.active_msg.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ChatUI()
    sys.exit(app.exec_())
