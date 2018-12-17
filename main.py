import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QListView, QApplication, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread, QStringListModel
from PyQt5.QtGui import QTextCursor, QColor

from alive import AliveMessager
from setting import *

# background messager instance
bg_msgr_ins = AliveMessager.create()


class MessageListener(QThread):
    answer = pyqtSignal(MyChatRole, str)

    def __init__(self, parent):
        super().__init__(parent)

    # override the super class method
    def run(self):
        while True:
            msg = bg_msgr_ins.get_msg()
            if isinstance(msg, str):
                self.answer.emit(role_anonym, msg)
            else:
                try:
                    print(f'UI message listener, unexpected msg : \"{msg}\"!')
                except AttributeError:
                    print(f'UI message listener, unexpected msg , No str property available!')


class MessageWorker(QObject):
    work_done = pyqtSignal(MyChatRole, str)

    def __init__(self):
        super().__init__()

    def do_work(self, msg: str):
        bg_msgr_ins.send_msg(msg)
        self.work_done.emit(role_sys, f"send message \"{msg}\" done.")


class MessageTransfer(QObject):
    transfer = pyqtSignal(str)
    message_done = pyqtSignal(MyChatRole, str)

    def __init__(self):
        super().__init__()
        self.__worker_thread = QThread()
        self.__worker = MessageWorker()
        self.__worker.moveToThread(self.__worker_thread)
        self.transfer.connect(self.__worker.do_work)
        self.__worker.work_done.connect(self.message_done)
        self.__worker_thread.start()

    def __del__(self):
        self.__worker_thread.quit()
        self.__worker_thread.wait()


class InputEdit(QTextEdit):
    enter_return = pyqtSignal(str)
    role_message = pyqtSignal(MyChatRole, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    # override slot
    def keyPressEvent(self, event):
        QTextEdit.keyPressEvent(self, event)
        key_code = event.key()
        if key_code == Qt.Key_Enter or key_code == Qt.Key_Return:
            # todo : to check shift key status
            msg = self.toPlainText().strip('\r\n')
            self.role_message.emit(role_user, msg)
            self.enter_return.emit(msg)
            self.setText("")

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        filename = urls[0].toLocalFile()
        self.insertPlainText(filename)


class OutputEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.role_message(role_sys, 'welcome!')

    def __enter_msg(self, msg):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(msg)

    # No signature slot
    def role_message(self, role: MyChatRole, msg: str):
        self.__enter_msg(role.role_msg(msg))


class ChatUI(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.transfer = MessageTransfer()
        self.listener = MessageListener(self)
        self.init_ui()

    def init_ui(self):
        h_box = QHBoxLayout(self)

        # the top left
        output_edit = OutputEdit(self)
        output_edit_bg_col = QColor(240, 250, 240)
        output_edit.setStyleSheet(f'background:{output_edit_bg_col.name()}')
        output_edit.setReadOnly(True)
        output_edit.setMinimumSize(400, 300)
        # the bottom left
        input_edit = InputEdit(self)
        input_edit.setMinimumHeight(50)
        input_edit.role_message.connect(output_edit.role_message)
        input_edit.enter_return.connect(self.transfer.transfer)
        # the right panel
        list_model = QStringListModel()
        list_model.setStringList([role_sys.role_name, role_anonym.role_name, role_user.role_name])
        chat_list = QListView(self)
        chat_list.setModel(list_model)

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

        # message transfer/listener threads
        self.transfer.message_done.connect(output_edit.role_message)
        self.listener.answer.connect(output_edit.role_message)
        self.listener.start()

        # the main window
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('My chat')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ChatUI()
    sys.exit(app.exec_())
