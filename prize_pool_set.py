#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: BCL
@license: Apache Licence 
@contact: 76332706@163.com
@site: http://www.sqstudio.com
@software: PyCharm
@file: prize_pool_set.py
@time: 2018-06-06 14:35
"""

from prize_pool_set_ui import Ui_Prize_Pool_Set
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSignal
import xml.etree.ElementTree as ET
import pathlib
import sys, os


class PrizePoolSet(QWidget):
    def __init__(self):
        super(PrizePoolSet, self).__init__()
        self.ui = Ui_Prize_Pool_Set()
        self.ui.setupUi(self)
        self._res_dict = {}
        self.open()

    def open(self):
        try:
            _c = [self.ui.lineEdit_c0, self.ui.lineEdit_c1, self.ui.lineEdit_c2, self.ui.lineEdit_c3,
                  self.ui.lineEdit_c4,
                  self.ui.lineEdit_c5, self.ui.lineEdit_c6, self.ui.lineEdit_c7, self.ui.lineEdit_c8,
                  self.ui.lineEdit_c9]
            _r = [self.ui.lineEdit_r0, self.ui.lineEdit_r1, self.ui.lineEdit_r2, self.ui.lineEdit_r3,
                  self.ui.lineEdit_r4,
                  self.ui.lineEdit_r5, self.ui.lineEdit_r6, self.ui.lineEdit_r7, self.ui.lineEdit_r8,
                  self.ui.lineEdit_r9]
            _xml_path = os.path.split(os.path.realpath(__file__))[0] + '/prize_pool_set.xml'
            _xml = ET.parse(_xml_path)
            _root = _xml.getroot()
            for _e in _root:
                for _ele in _e.iter('count'):
                    _text = _ele.text if _ele.text != None else '0'
                _c[int(_e.get('level'))].setText(_text)
                for _ele in _e.iter('range'):
                    _text = _ele.text[2:-2] if _ele.text != None else '0'
                _r[int(_e.get('level'))].setText(_text)
        except Exception as e:
            return

    def save(self):
        _xml_path = os.path.split(os.path.realpath(__file__))[0] + '/prize_pool_set.xml'
        if not pathlib.Path(_xml_path).exists():
            _xml = ET.Element('prize_pool_set')
            for _i in range(0, 10):
                _node = ET.SubElement(_xml, 'prize', {'level': str(_i)})
                ET.SubElement(_node, 'count')
                ET.SubElement(_node, 'range')
            et = ET.ElementTree(_xml)
            et.write(_xml_path, encoding='utf-8', xml_declaration=True)

        _xml = ET.parse(_xml_path)
        _root = _xml.getroot()

        _update_flag = False
        self.get_resust()
        for _k, _v in self._res_dict.items():
            for _child in _root.iter('prize'):
                if _child.get('level') == (str(_k)):
                    for _c in _child.iter('count'):
                        _c.text = str(_v['count']) if _v['count'] != None else '0'
                    for _c in _child.iter('range'):
                        _c.text = str(_v['range'].split(',')) if _v['range'] != None else '0'
                    _xml.write(_xml_path, encoding='utf-8', xml_declaration=True)
                    _update_flag = True

            if not _update_flag:
                _node = ET.SubElement(_root, 'prize', {'level': str(_k)})
                _count = ET.SubElement(_node, 'count')
                # print(_v['count'])
                _count.text = _v['count'] if not _v['count'] else '0'
                _range = ET.SubElement(_node, 'range')
                _range.text = str(_v['range'].split(',')) if not _v['range'] else '0'
                # _root.append(_node)
                _xml.write('prize_pool_set.xml', encoding='utf-8', xml_declaration=True)
        self.close()
        ET.dump(_xml)

    def get_resust(self):
        self._res_dict[0] = {'count': self.ui.lineEdit_c0.text(), 'range': self.ui.lineEdit_r0.text()}
        self._res_dict[1] = {'count': self.ui.lineEdit_c1.text(), 'range': self.ui.lineEdit_r1.text()}
        self._res_dict[2] = {'count': self.ui.lineEdit_c2.text(), 'range': self.ui.lineEdit_r2.text()}
        self._res_dict[3] = {'count': self.ui.lineEdit_c3.text(), 'range': self.ui.lineEdit_r3.text()}
        self._res_dict[4] = {'count': self.ui.lineEdit_c4.text(), 'range': self.ui.lineEdit_r4.text()}
        self._res_dict[5] = {'count': self.ui.lineEdit_c5.text(), 'range': self.ui.lineEdit_r5.text()}
        self._res_dict[6] = {'count': self.ui.lineEdit_c6.text(), 'range': self.ui.lineEdit_r6.text()}
        self._res_dict[7] = {'count': self.ui.lineEdit_c7.text(), 'range': self.ui.lineEdit_r7.text()}
        self._res_dict[8] = {'count': self.ui.lineEdit_c8.text(), 'range': self.ui.lineEdit_r8.text()}
        self._res_dict[9] = {'count': self.ui.lineEdit_c9.text(), 'range': self.ui.lineEdit_r9.text()}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pps = PrizePoolSet()
    pps.show()
    sys.exit(app.exec_())
