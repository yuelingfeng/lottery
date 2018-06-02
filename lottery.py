from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from lottery_ui import Ui_Main
import random
import time


class Lottery(QWidget):
    def __init__(self, parent=None):
        super(Lottery, self).__init__(parent)
        self.ui = Ui_Main()
        self.ui.setupUi(self)
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
        self._position = {
            '0': [2],
            '1': [5],
            '2': [3],
            '3': [0],
            '4': [7],
            '5': [1, 4, 6]
        }
        # 结果列表
        self._value_list = ''
        # 初始化奖池
        self.prize_pool()

    def lottery_start(self):
        if self._press and not self._run_flag:
            self.start_v()
            self.start_thread = MyThread()
            self.start_thread.time_change_signal.connect(self.update)
            self.start_thread.start()
        else:
            self.end_v()
            self.start_thread.stop()
            self._stop_thread = MyThreadStop()
            self._stop_thread.time_change_signal.connect(self.update)
            self._stop_thread.start()
        # self.prize_test()

    def update(self, _b):
        _label_list = [self.ui.label_r1, self.ui.label_r2, self.ui.label_r3, self.ui.label_r4,
                       self.ui.label_r5, self.ui.label_r6,
                       self.ui.label_r7, self.ui.label_r8]
        _border_normal_style = 'border:1px solid black;border-radius:5px'
        _border_choose_style = 'border:5px solid black;border-radius:5px;border-color:rgb(255 ,127, 36);'

        if _b:
            if self._index == 0:
                _label_list[self._index].setStyleSheet(_border_choose_style)
                _label_list[7].setStyleSheet(_border_normal_style)
            else:
                _label_list[self._index - 1].setStyleSheet(_border_normal_style)
                _label_list[self._index].setStyleSheet(_border_choose_style)
            if self._index == 7:
                self._index = 0
            else:
                self._index += 1

            if self._stop:
                self._stop_time += 0.3

            if self._stop_time > 3 and self._stop and self._index == self._stop_index:
                self._stop_thread.stop()

        else:
            self._value_list = self._value_list + u'恭喜您，抽中了%s等奖!' % \
                               _label_list[self._stop_index].text() + '\n'
            self.setlistvalue(self._value_list)
            self.ui.pushButton.setEnabled(True)
            self._stop_thread.terminate()

    def start_v(self):
        self._run_flag = True
        self._stop = False
        self._stop_index = 9
        self._stop_time = 0.00
        self._press = False
        _prize = random.choice(self._prize_pool)
        self._prize_pool.remove(_prize)
        self._stop_index = random.choice(self._position[_prize])

    def setlistvalue(self, text):
        self.ui.textEdit.setText(text)

    def end_v(self):
        self.ui.pushButton.setEnabled(False)
        self._stop = True
        self._run_flag = False
        self._press = True


    def prize_pool(self):
        _prize_dict = {
            '0': 1,
            '1': 1,
            '2': 2,
            '3': 5,
            '4': 10,
            '5': 5000,
        }
        for _k, _v in _prize_dict.items():
            _temp = [_k] * _v
            self._prize_pool = self._prize_pool + _temp
        random.shuffle(self._prize_pool)

    def prize_test(self):
        _i = 0
        _res_dict = {
            '0': 0,
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
        }
        while _i < 1000:
            if len(self._prize_pool) == 0:
                print('奖池没有奖了')
                break
            p = random.choice(self._prize_pool)
            self._prize_pool.remove(p)
            if p == '0':
                print(_i)
            _i += 1
            _res_dict[p] += 1
        print(_res_dict)


class MyThread(QThread):
    time_change_signal = pyqtSignal(bool)

    def __init__(self):
        super(MyThread, self).__init__()
        self._stop = False

    def run(self):
        # self.ui.label_r4.setStyleSheet(_border_choose_style)
        while not self._stop:
            self.time_change_signal.emit(True)
            time.sleep(0.06)

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
