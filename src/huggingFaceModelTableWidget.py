import typing

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QLabel


class HuggingFaceModelTableWidget(QTableWidget):
    def __init__(self):
        super(HuggingFaceModelTableWidget, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__header_labels = {v: i for (i, v) in enumerate(['Name', 'Size', 'Text2Image?', 'Visit'])}

    def __initUi(self):
        self.setHorizontalHeaderLabels(self.__header_labels.keys())
        self.resizeColumnsToContents()
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

            model_id = model['id'] if isinstance(model, dict) else model

            # id
            if self.__header_labels.get('Name', '') != '':
                model_id_item = QTableWidgetItem(model_id)
                model_id_item.setTextAlignment(Qt.AlignCenter)
                self.setItem(cur_table_idx, self.__header_labels['Name'], model_id_item)

            # size on disk
            if self.__header_labels.get('Size', '') != '':
                size_on_disk_str = model['size_on_disk_str']
                size_on_disk_str_item = QTableWidgetItem(size_on_disk_str)
                size_on_disk_str_item.setTextAlignment(Qt.AlignCenter)
                self.setItem(cur_table_idx, self.__header_labels['Size'], size_on_disk_str_item)

            # is text2image or something else
            if self.__header_labels.get('Text2Image?', '') != '':
                is_t2i = 'Yes' if model['is_t2i'] else 'No'
                is_t2i_item = QTableWidgetItem(is_t2i)
                is_t2i_item.setTextAlignment(Qt.AlignCenter)
                self.setItem(cur_table_idx, self.__header_labels['Text2Image?'], is_t2i_item)

            # visit
            if self.__header_labels.get('Visit', '') != '':
                hyperlink_tag = f'<a href="https://huggingface.co/{model_id}">Link</a>'
                self.set_hyperlink(cur_table_idx, self.__header_labels['Visit'], hyperlink_tag)

            self.setCurrentCell(0, 0)

        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sortByColumn(0, Qt.AscendingOrder)

    def setHorizontalHeaderLabels(self, labels: typing.Iterable[str]) -> None:
        self.__header_labels = {v: i for (i, v) in enumerate(labels)}
        self.setColumnCount(len(self.__header_labels))
        super(HuggingFaceModelTableWidget, self).setHorizontalHeaderLabels(self.__header_labels.keys())

    def getCurrentRowModelName(self):
        return self.item(self.currentRow(), 0).text()