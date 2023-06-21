from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFrame, QPushButton, QHBoxLayout, QWidget, QApplication, QLabel, \
    QSpacerItem, QSizePolicy, QMessageBox

from src.huggingFaceModelClass import HuggingFaceModelClass
from src.huggingFaceModelLoadingWidget import HuggingFaceModelLoadingWidget


class HuggingFaceModelInputDialog(QDialog):
    def __init__(self, hf_class, parent=None):
        super().__init__(parent)
        self.__initVal(hf_class)
        self.__initUi()

    def __initVal(self, hf_class):
        self.__hf_class = hf_class
        self.__model = ''

    def __initUi(self):
        self.setWindowTitle('New...')
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        huggingFaceModelLoadingWidget = HuggingFaceModelLoadingWidget(self.__hf_class)
        huggingFaceModelLoadingWidget.onInstalled.connect(self.__setAccept)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        self.__criticalLbl = QLabel()
        self.__criticalLbl.setStyleSheet("color: {}".format(QColor(255, 0, 0).name()))

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)

        lay = QHBoxLayout()
        lay.addWidget(self.__criticalLbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(cancelBtn)
        lay.setAlignment(Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(huggingFaceModelLoadingWidget)
        lay.addWidget(sep)
        lay.addWidget(bottomWidget)

        self.setLayout(lay)

    def getModel(self):
        return self.__model

    def __setAccept(self, model: dict):
        self.__model = model
        self.accept()


if __name__ == '__main__':
    import sys

    hf_class = HuggingFaceModelClass()
    app = QApplication(sys.argv)
    w = HuggingFaceModelInputDialog(hf_class)
    w.show()
    sys.exit(app.exec())
