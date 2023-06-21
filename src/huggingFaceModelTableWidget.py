from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QLabel


class HuggingFaceModelTableWidget(QTableWidget):
    def __init__(self):
        super(HuggingFaceModelTableWidget, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.setColumnCount(3)
        self.resizeColumnsToContents()
        self.setHorizontalHeaderLabels(['Name', 'Size', 'Visit'])
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def set_hyperlink(self, row, column, text):
        label = QLabel(text)
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignCenter)
        self.setCellWidget(row, column, label)

    def addModels(self, models: list):
        for i in range(len(models)):
            cur_table_idx = self.rowCount()

            self.setRowCount(cur_table_idx+1)
            model = models[i]

            # id
            model_id = model['id'] if isinstance(model, dict) else model
            model_id_item = QTableWidgetItem(model_id)
            model_id_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(cur_table_idx, 0, model_id_item)

            # size on disk
            size_on_disk_str = model['size_on_disk_str']
            size_on_disk_str_item = QTableWidgetItem(size_on_disk_str)
            size_on_disk_str_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(cur_table_idx, 1, size_on_disk_str_item)

            # visit
            hyperlink_tag = f'<a href="https://huggingface.co/{model_id}">Link</a>'
            self.set_hyperlink(cur_table_idx, 2, hyperlink_tag)

            self.setCurrentItem(model_id_item)

        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def getCurrentRowModelName(self):
        return self.item(self.currentRow(), 0).text()