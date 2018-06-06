from lottery_set_ui import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSignal
import xml.etree.ElementTree as ET
import pathlib
import sys, os


class LotterSet(QWidget):
    updateset = pyqtSignal()

    def __init__(self, objname, parent=None):
        super(LotterSet, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.lineEdit_4.setText(objname)
        self.ui.lineEdit_4.setEnabled(False)
        self.init_commbobox()

    def init_commbobox(self):
        _combobox_value_list = ['特等奖', '一等奖', '二等奖', '三等奖', '四等奖',
                                '五等奖', '六等奖', '7等奖', '八等奖', '幸运奖']
        for _e in _combobox_value_list:
            self.ui.comboBox.addItem(_e)

    def open_file_path(self):
        _file = QFileDialog.getOpenFileNames()
        if len(_file[0]) > 0:
            self.ui.lineEdit_2.setText(_file[0][0])

    def save_set(self):
        _update_flag = False
        _position = self.ui.lineEdit_4.text()
        _description = self.ui.lineEdit.text()
        _img_path = self.ui.lineEdit_2.text()
        _prize = str(self.ui.comboBox.currentIndex())
        _xml_path = os.path.split(os.path.realpath(__file__))[0] + '/lottery_set.xml'
        if not pathlib.Path(_xml_path).exists():
            _root = ET.Element('Lottery_Set')
            _node = ET.SubElement(_root, 'position', {'pos': _position})
            description = ET.SubElement(_node, 'description')
            description.text = _description
            img_path = ET.SubElement(_node, 'img_path')
            img_path.text = _img_path
            prize = ET.SubElement(_node, 'prize',{'type': 'int'})
            prize.text = _prize
            et = ET.ElementTree(_root)
            et.write('lottery_set.xml', encoding='utf-8', xml_declaration=True)
            self.updateset.emit()
            self.close()

        _xml = ET.parse(_xml_path)
        _root = _xml.getroot()

        for _child in _root:
            if _child.get('pos') == _position:
                for description in _child.iter('description'):
                    description.text = _description
                for img_path in _child.iter('img_path'):
                    img_path.text = _img_path
                for prize in _child.iter('prize'):
                    prize.text = _prize
                _xml.write(_xml_path,encoding='utf-8', xml_declaration=True)
                _update_flag = True

        if not _update_flag:
            _child = ET.SubElement(_root, 'position', {'pos': _position})
            description = ET.SubElement(_child, 'description')
            description.text = _description
            img_path = ET.SubElement(_child, 'img_path')
            img_path.text = _img_path
            prize = ET.SubElement(_child, 'prize', {'type': 'int'})
            prize.text = str(_prize)
            # _root.append(_child)
            _xml.write('lottery_set.xml', encoding='utf-8', xml_declaration=True)
        # ET.dump(_xml)
        self.updateset.emit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ls = LotterSet('aa')
    ls.show()
    sys.exit(app.exec_())
