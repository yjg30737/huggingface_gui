from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QMessageBox

from src.huggingFaceModelClass import HuggingFaceModelClass


class InstallModelThread(QThread):
    installFinished = pyqtSignal(dict)
    installFailed = pyqtSignal(str)

    def __init__(self, hf_class: HuggingFaceModelClass, model_name_to_install: str):
        super(InstallModelThread, self).__init__()
        self.__hf_class = hf_class
        self.__model_name_to_install = model_name_to_install

    def run(self):
        try:
            if self.__model_name_to_install in [model['id'] for model in self.__hf_class.getModels()]:
                raise Exception('Model already exists.')
            else:
                self.installFinished.emit(self.__hf_class.installHuggingFaceModel(self.__model_name_to_install)[0])
        except Exception as e:
            self.installFailed.emit(str(e))


class HuggingFaceModelLoadingWidget(QWidget):
    onInstalled = pyqtSignal(dict)

    def __init__(self, hf_class):
        super(HuggingFaceModelLoadingWidget, self).__init__()
        self.__initVal(hf_class)
        self.__initUi()

    def __initVal(self, hf_class):
        self.__hf_class = hf_class

    def __initUi(self):
        self.__newModelLineEdit = QLineEdit()

        self.__installBtn = QPushButton('Use')
        self.__installBtn.clicked.connect(self.__installModel)

        self.__newModelLineEdit.textChanged.connect(self.__installBtnActivated)

        lay = QHBoxLayout()
        lay.addWidget(self.__newModelLineEdit)
        lay.addWidget(self.__installBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        self.__loadingLbl = QLabel()

        lay = QHBoxLayout()
        lay.addWidget(self.__loadingLbl)
        lay.setAlignment(Qt.AlignLeft)
        lay.setContentsMargins(0, 0, 0, 0)

        self.__bottomWidget = QWidget()
        self.__bottomWidget.setLayout(lay)
        self.__bottomWidget.setVisible(False)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(self.__bottomWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def __installBtnActivated(self, text):
        self.__installBtn.setEnabled(text.strip() != '')

    def __installModel(self):
        self.__t = InstallModelThread(self.__hf_class, self.__newModelLineEdit.text())

        self.__t.started.connect(self.thread_started)
        self.__t.finished.connect(self.thread_finished)
        self.__t.finished.connect(self.__t.deleteLater)
        self.__t.installFinished.connect(self.__installFinished)
        self.__t.installFailed.connect(self.__installFailed)
        self.__t.start()

    def thread_started(self):
        self.__loadingLbl.setText('Installing...')
        self.__bottomWidget.setVisible(True)

    def thread_finished(self):
        self.__bottomWidget.setVisible(False)
        self.__installBtn.setEnabled(False)

    def __installFinished(self, model: dict):
        self.onInstalled.emit(model)

    def __installFailed(self, err_msg):
        self.__installBtn.setEnabled(True)
        QMessageBox.critical(self, "Error", err_msg)


# if __name__ == '__main__':
#     import sys
#
#     hf_class = HuggingFaceModelClass()
#     app = QApplication(sys.argv)
#     w = HuggingFaceModelLoadingWidget(hf_class)
#     w.show()
#     sys.exit(app.exec())
