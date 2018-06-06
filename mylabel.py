from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal


class MyLabel(QLabel):
    label_double_click = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self._name = ''

    def mouseDoubleClickEvent(self, e):
        self.label_double_click.emit(self.objectName())

    def setName(self, name):
        if name:
            self._name = name
        else:
            self._name = self.text()

    def name(self):
        return self._name
