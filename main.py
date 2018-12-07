import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QListWidget, QApplication, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor

from alive import MessageMemory


class FileSystemSensor:
    pass


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
        self.msg_receiver = MessageReceiver()
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
        input_edit.sig_input.connect(self.msg_receiver.on_input)
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
        self.setWindowTitle('Ape chatting')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ChatUI()
    sys.exit(app.exec_())
