import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel


class ExampleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('sample')

        # buttonの設定
        self.button = QPushButton('Clear!!')
        self.label = QLabel('connected')

        # buttonのclickでラベルをクリア
        self.button.clicked.connect(self.label.clear)

        # レイアウト配置
        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 0, 1, 1)
        self.grid.addWidget(self.label, 1, 0, 1, 2)
        self.setLayout(self.grid)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ew = ExampleWidget()
    sys.exit(app.exec_())
