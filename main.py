import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QSplitter, QListWidget, QApplication, QTextEdit)
from PyQt5.QtCore import Qt


class ChatUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        h_box = QHBoxLayout(self)

        # the top left
        output_edit = QTextEdit(self)
        output_edit.setReadOnly(True)
        output_edit.setMinimumSize(400, 300)
        # the bottom left
        input_edit = QTextEdit(self)
        input_edit.setMinimumHeight(50)
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
