import sys
from PyQt5.QtWidgets import QApplication
from lottery import Lottery

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lo = Lottery()
    lo.show()
    sys.exit(app.exec_())
