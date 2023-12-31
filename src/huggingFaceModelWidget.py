import os
import sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from src.huggingFacePathWidget import FindPathWidget

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QPushButton, QDialog, QMessageBox

from src.huggingFaceModelClass import HuggingFaceModelClass
from src.huggingFaceModelInputDialog import HuggingFaceModelInputDialog
from src.huggingFaceModelTableWidget import HuggingFaceModelTableWidget

QApplication.setWindowIcon(QIcon('hf-logo.svg'))


class HuggingFaceModelWidget(QWidget):
    onModelAdded = pyqtSignal(str)
    onModelDeleted = pyqtSignal(str)
    onModelSelected = pyqtSignal(str)
    onCacheDirSet = pyqtSignal(str)

    def __init__(self, certain_models=None, parent=None):
        super(HuggingFaceModelWidget, self).__init__(parent)
        self.__initVal(certain_models)
        self.__initUi()

    def __initVal(self, certain_models):
        self.__certain_models = certain_models
        self.__total_size_prefix = 'Total:'

    def __initUi(self):
        self.setWindowTitle('HuggingFace Model Table')

        self.__findPathWidget = FindPathWidget()
        self.__cache_dir = self.__findPathWidget.getCacheDirectory()
        self.__findPathWidget.onCacheDirSet.connect(self.setCacheDir)

        self.__resetBtn = QPushButton('Reset Cache Directory')
        self.__resetBtn.clicked.connect(self.__resetCacheDir)

        self.__addBtn = QPushButton('Add')
        self.__delBtn = QPushButton('Delete')

        self.__addBtn.clicked.connect(self.__addClicked)
        self.__delBtn.clicked.connect(self.__deleteClicked)

        lay = QHBoxLayout()

        lay.addWidget(QLabel('Model Table'))
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(QLabel('Cache Directory'))
        lay.addWidget(self.__findPathWidget)
        lay.addWidget(self.__resetBtn)
        lay.addWidget(self.__addBtn)
        lay.addWidget(self.__delBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        menuWidget = QWidget()
        menuWidget.setLayout(lay)

        self.__hf_class = HuggingFaceModelClass()

        self.__modelTableWidget = HuggingFaceModelTableWidget()
        self.__modelTableWidget.currentCellChanged.connect(self.__currentCellChanged)

        self.__totalSizeLbl = QLabel()
        self.__totalSizeLbl.setAlignment(Qt.AlignRight)

        self.setCacheDir(self.__cache_dir)

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
                self.__totalSizeLbl.setText(f'{self.__total_size_prefix} {self.__hf_class.getModelsSize(self.__certain_models)}')
                self.onModelAdded.emit(model)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def __deleteClicked(self):
        model_name = self.__modelTableWidget.getCurrentRowModelName()
        self.__hf_class.removeHuggingFaceModel(model_name)
        cur_row = self.__modelTableWidget.currentRow()
        self.__modelTableWidget.removeRow(cur_row)
        self.__totalSizeLbl.setText(f'{self.__total_size_prefix} {self.__hf_class.getModelsSize(self.__certain_models)}')
        self.__modelTableWidget.setCurrentCell(max(0, min(cur_row, self.__modelTableWidget.rowCount()-1)), 0)
        self.__delBtn.setEnabled(self.__modelTableWidget.rowCount() != 0)
        self.onModelDeleted.emit(model_name)

    def __currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        cur_item = self.__modelTableWidget.item(currentRow, 0)
        if cur_item:
            self.__delBtn.setEnabled(True)
            cur_model_name = cur_item.text()
            self.onModelSelected.emit(cur_model_name)
        else:
            self.__delBtn.setEnabled(False)

    def __resetCacheDir(self):
        self.__findPathWidget.resetCacheDir()

    def setCacheDir(self, cache_dir):
        self.__cache_dir = cache_dir
        self.__modelTableWidget.clearContents()
        self.__modelTableWidget.setRowCount(0)
        self.__hf_class.setCacheDir(self.__cache_dir)
        models = self.__hf_class.getModels(self.__certain_models)
        if len(models) == 0:
            self.__delBtn.setEnabled(False)
        self.__modelTableWidget.addModels(models)
        self.__totalSizeLbl.setText(f'{self.__total_size_prefix} {self.__hf_class.getModelsSize(self.__certain_models)}')
        self.onCacheDirSet.emit(cache_dir)

    def getCurrentModelName(self):
        cur_item = self.__modelTableWidget.item(self.__modelTableWidget.currentRow(), 0)
        cur_model_name = ''
        if cur_item:
            cur_model_name = cur_item.text()
        return cur_model_name

    def getCurrentModelObject(self):
        """
        after called this, you should use from_pretrained
        :return:
        """
        return self.__hf_class.getModelObject(self.getCurrentModelName())

    def getCertainModelObject(self, model_name):
        """
        after called this, you should use from_pretrained
        :return:
        """
        return self.__hf_class.getModelObject(model_name)

    def getModelTable(self):
        return self.__modelTableWidget

    def selectCurrentModel(self, model_name):
        """
        select the row which has "model_name" as an Name
        """
        items = self.__modelTableWidget.findItems(model_name, Qt.MatchExactly)
        if len(items) > 0:
            self.__modelTableWidget.setCurrentCell(items[0].row(), 0)

    def getModelClass(self):
        return self.__hf_class


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = HuggingFaceModelWidget()
    w.show()
    sys.exit(app.exec())
