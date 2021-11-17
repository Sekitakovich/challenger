import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget
# PySide2の時はPySide6.QtWidgets.QActionだった。
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtWidgets import QLineEdit, QLabel, QPushButton
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("サンプルGUIアプリ")
        self.resize(QSize(500, 400))

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("終了", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Status...")

        self.__controls()
        self.__layout()

    def __controls(self):
        self.lbl_01 = QLabel("名前")
        self.txt_01 = QLineEdit()
        self.btn_load = QPushButton("変換", self)
        self.btn_load.clicked.connect(self.on_btn_clicked)

        self.lbl_contents = QLabel("")
        self.lbl_contents.setTextFormat(Qt.RichText)
        self.lbl_contents.setWordWrap(True)
        self.lbl_contents.setStyleSheet("border:1px solid black;padding:10px;line-height: 0.5px;")
        self.lbl_contents.setText('')

    def __layout(self):
        self.main_widget = QWidget(self)

        self.v_box = QVBoxLayout()
        self.h_box = QHBoxLayout()
        self.h_contents = QHBoxLayout()

        self.h_box.addWidget(self.lbl_01)
        self.h_box.addWidget(self.txt_01)
        self.h_box.addWidget(self.btn_load)

        self.h_contents.addWidget(self.lbl_contents)

        self.v_box.addLayout(self.h_box)
        self.v_box.addLayout(self.h_contents)

        self.main_widget.setLayout(self.v_box)

        self.setCentralWidget(self.main_widget)

    @Slot()
    def exit_app(self, checked):
        sys.exit()

    def on_btn_clicked(self):
        print("call on_btn_clicked")

        self.lbl_contents.setText('Hello ' + self.txt_01.text())
