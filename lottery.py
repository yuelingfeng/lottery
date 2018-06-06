from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from lottery_ui import Ui_Main
from lottery_set import LotterSet
import random
import time, os
import xml.etree.ElementTree as ET


class Lottery(QWidget):
    def __init__(self, parent=None):
        super(Lottery, self).__init__(parent)
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        # 抽奖序号，用于区分每一次抽奖
        self.prize_index = 0
        # 出奖范围
        self.prize_range = {}
        # 必出奖
        self._must_dict = {}

        self._label_lists = [self.ui.label_r00, self.ui.label_r01, self.ui.label_r02, self.ui.label_r03,
                             self.ui.label_r04, self.ui.label_r05, self.ui.label_r06, self.ui.label_r07,
                             self.ui.label_r08, self.ui.label_r09, self.ui.label_r10, self.ui.label_r11,
                             ]

        # 当前抽中框所在位置
        self._index = 0
        # 按钮是开始状态还是停止状态
        self._press = True
        # 是否按下了停止
        self._stop = False
        # 中奖位置
        self._stop_index = 0
        # 抽奖还是等待状态
        self._run_flag = False
        # 按下停止后还需要多少时间
        self._stop_time = 0.00
        # 抽奖吃
        self._prize_pool = []
        # 奖项位置
        self._position = {}
        self.prize_positon()
        # 结果列表
        self._value_list = ''
        # 初始化奖池
        self.prize_pool()
        # 初始化label
        self.init_label()

    def prize_positon(self):
        _xml_path = os.path.split(os.path.realpath(__file__))[0] + '/lottery_set.xml'
        _xml = ET.parse(_xml_path)
        _root = _xml.getroot()

        for _e in _root:
            _index = -1
            for _o in self._label_lists:
                if _o.objectName() == _e.get('pos'):
                    _index = self._label_lists.index(_o)
                    break
            for _ele in _e.iter('prize'):
                if _index >= 0:
                    if _ele.text in self._position.keys():
                        self._position[_ele.text].append(_index)
                    else:
                        self._position[_ele.text] = []
                        self._position[_ele.text].append(_index)

    def lottery_start(self):
        if self._press and not self._run_flag:
            self.start_v()
            self.start_thread = MyThread()
            self.start_thread.time_change_signal.connect(self.update)
            self.start_thread.auto_stop_signal.connect(self.ui.pushButton.click)
            self.start_thread.start()
        else:
            self.end_v()
            self.start_thread.stop()
            self._stop_thread = MyThreadStop()
            self._stop_thread.time_change_signal.connect(self.update)
            self._stop_thread.start()
        # self.prize_test()

    def update(self, _b):
        _label_list = self._label_lists
        _border_normal_style = 'border:1px solid black;border-radius:5px'
        _border_choose_style = 'border:5px solid black;border-radius:5px;border-color:rgb(255 ,127, 36);'

        if _b:
            if self._index == 0:
                _label_list[self._index].setStyleSheet(_border_choose_style)
                _label_list[11].setStyleSheet(_border_normal_style)
            else:
                _label_list[self._index - 1].setStyleSheet(_border_normal_style)
                _label_list[self._index].setStyleSheet(_border_choose_style)
            if self._index == 11:
                self._index = 0
            else:
                self._index += 1

            if self._stop:
                self._stop_time += 0.3

            if self._stop_time > 3.6 and self._stop and self._index == self._stop_index:
                self._stop_thread.stop()

        else:
            self._value_list = self._value_list + u'恭喜您，抽中了%s!' % \
                               _label_list[self._stop_index].name() + '\n'
            self.setlistvalue(self._value_list)
            self.ui.pushButton.setEnabled(True)
            self._stop_thread.terminate()

    def start_v(self):
        self._run_flag = True
        self._stop = False
        self._stop_index = 9
        self._stop_time = 0.00
        self._press = False
        self.prize_index += 1
        self._stop_index = self._draw()

    def _draw(self):
        _prize = random.choice(self._prize_pool)
        # print(_prize,self.prize_range[_prize],self.prize_index)
        for _k, _v in self._must_dict.items():
            if _v == self.prize_index:
                self._prize_pool.remove(_k)
                return random.choice(self._position[_k])
        if self.prize_index in self.prize_range[_prize]:
            self._prize_pool.remove(_prize)
            return random.choice(self._position[_prize])
        else:
            return self._draw()

    def setlistvalue(self, text):
        self.ui.textEdit.setText(text)

    def end_v(self):
        self.ui.pushButton.setEnabled(False)
        self._stop = True
        self._run_flag = False
        self._press = True

    def prize_pool(self):
        _xml_path = os.path.split(os.path.realpath(__file__))[0] + '/prize_pool_set.xml'
        _xml = ET.parse(_xml_path)
        _root = _xml.getroot()
        _prize_dict = {}

        for _e in _root:
            for _el in _e.iter('range'):
                if _el.text[2:-2] in [None, '', 0, '0']:
                    self.prize_range[_e.get('level')] = [i for i in range(0, 10000)]
                else:
                    _temp = _el.text[2:-2].split('-')
                    _start_num = int(_temp[0])
                    if len(_temp) > 1:
                        _end_num = int(_temp[1]) + 1
                    else:
                        _end_num = int(_temp[0]) + 1
                    self.prize_range[_e.get('level')] = [i for i in range(_start_num, _end_num)]

            for _ele in _e.iter('count'):
                _prize_dict[_e.get('level')] = int(_ele.text)
        for _k, _v in _prize_dict.items():
            if _v == 0:
                continue
            _temp = [_k] * _v
            self._prize_pool = self._prize_pool + _temp
        random.shuffle(self._prize_pool)

        for _k, _v in self.prize_range.items():
            self._must_dict[_k] = _v[-1]

    def prize_test(self):
        _i = 0
        while _i < 5000:
            self.prize_index += 1
            if len(self._prize_pool) == 0:
                print('奖池没有奖了')
                break
            p = self._draw()
            if p in self._position['0']:
                print(_i, p)
                print('0',len(self._prize_pool))
            if p in self._position['1']:
                print(_i, p)
                print('1', len(self._prize_pool))
            if p in self._position['2']:
                print(_i, p)
                print('2', len(self._prize_pool))
            _i += 1

    def label_doubl_cleck(self, objname):
        self._lottery_set = LotterSet(objname=objname)
        self._lottery_set.updateset.connect(self.init_label)
        self._lottery_set.show()

    def init_label(self):
        try:
            _tree = ET.parse('lottery_set.xml')
            _root = _tree.getroot()
            _label_dict = {}
            for _c in _root.iter('position'):
                _c_label_dict = {}
                for _cc in _c:
                    _c_label_dict[_cc.tag] = _cc.text
                _label_dict[_c.get('pos')] = _c_label_dict
            for obj in self._label_lists:
                _obj = obj.objectName()
                if _obj in _label_dict.keys():
                    _text = str(_label_dict[_obj]['description'])
                    obj.setName(_text)
                    obj.setText(_text)
                    if _label_dict[_obj]['img_path']:
                        _img = QPixmap(_label_dict[_obj]['img_path'])
                        _img = _img.scaled(275, 275)
                        obj.setPixmap(_img)
                    # obj.setScaledContents(True)
        except Exception as e:
            print(e)
            pass


class MyThread(QThread):
    time_change_signal = pyqtSignal(bool)
    auto_stop_signal = pyqtSignal()

    def __init__(self):
        super(MyThread, self).__init__()
        self._stop = False

    def run(self):
        # self.ui.label_r4.setStyleSheet(_border_choose_style)
        _sec = 0
        while not self._stop:
            if _sec < 10:
                self.time_change_signal.emit(True)
                _sec += 0.06
                time.sleep(0.06)
            else:
                self.auto_stop_signal.emit()

    def stop(self):
        self.terminate()


class MyThreadStop(QThread):
    time_change_signal = pyqtSignal(bool)

    def __init__(self):
        super(MyThreadStop, self).__init__()
        self._stop = False
        self._sec = 0.06

    def run(self):
        # self.ui.label_r4.setStyleSheet(_border_choose_style)
        while not self._stop:
            time.sleep(self._sec)
            self.time_change_signal.emit(True)
            self._sec = self._sec + 0.02
        else:
            time.sleep(self._sec)
            self.time_change_signal.emit(False)

    def stop(self):
        self._stop = True
