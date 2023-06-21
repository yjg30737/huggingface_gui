import os, sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QPushButton, QDialog, QMessageBox

from src.huggingFaceModelClass import HuggingFaceModelClass
from src.huggingFaceModelInputDialog import HuggingFaceModelInputDialog
from src.huggingFaceModelTableWidget import HuggingFaceModelTableWidget

QApplication.setWindowIcon(QIcon('hf-logo.svg'))


class HuggingFaceModelWidget(QWidget):
    def __init__(self):
        super(HuggingFaceModelWidget, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__total_size_prefix = 'Total:'

    def __initUi(self):
        self.setWindowTitle('HuggingFace Model Table')
        self.__addBtn = QPushButton('Add')
        self.__delBtn = QPushButton('Delete')

        self.__addBtn.clicked.connect(self.__addClicked)
        self.__delBtn.clicked.connect(self.__deleteClicked)

        lay = QHBoxLayout()

        lay.addWidget(QLabel('Model Table'))
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(self.__addBtn)
        lay.addWidget(self.__delBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        menuWidget = QWidget()
        menuWidget.setLayout(lay)

        self.__hf_class = HuggingFaceModelClass()
        models = self.__hf_class.getAllInstalledModel()

        self.__modelTableWidget = HuggingFaceModelTableWidget()
        self.__modelTableWidget.addModels(models)

        self.__totalSizeLbl = QLabel(f'{self.__total_size_prefix} {self.__hf_class.getTotalSize()}')
        self.__totalSizeLbl.setAlignment(Qt.AlignRight)

        lay = QVBoxLayout()
        lay.addWidget(menuWidget)
        lay.addWidget(self.__modelTableWidget)
        lay.addWidget(self.__totalSizeLbl)

        self.setLayout(lay)

        self.resize(640, 300)

    def __addClicked(self):
        dialog = HuggingFaceModelInputDialog(self.__hf_class)
        reply = dialog.exec()
        if reply == QDialog.Accepted:
            try:
                model = dialog.getModel()
                # add model in the table
                self.__modelTableWidget.addModels([model])
                self.__totalSizeLbl.setText(f'{self.__total_size_prefix} {self.__hf_class.getTotalSize()}')
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def __deleteClicked(self):
        self.__hf_class.removeHuggingFaceModel(self.__modelTableWidget.getCurrentRowModelName())
        self.__modelTableWidget.removeRow(self.__modelTableWidget.currentRow())

        self.__totalSizeLbl.setText(f'{self.__total_size_prefix} {self.__hf_class.getTotalSize()}')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = HuggingFaceModelWidget()
    w.show()
    sys.exit(app.exec())
