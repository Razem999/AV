import can
import time
import datetime
from datetime import datetime
import sys
from PyQt5.QtCore import Qt, QTimer,QTime
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QWidget,QVBoxLayout
class Data(QObject):
    speed_changed = pyqtSignal(int)
    mode_changed = pyqtSignal(str)

class Dashboard(QMainWindow):
    def __init__(self, data):
        super(Dashboard, self).__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Car Dashboard')
        self.speed_label = QLabel('Speed: 0 km/h', self)
        self.speed_label = setA
        self.mode_label = QLabel('Mode: Manual', self)

        grid = QGridLayout()
        # grid.addWidget(self.title_label, 0,1)
        grid.addWidget(self.mode_label, 1, 0)
        grid.addWidget(self.speed_label, 1, 1)
    
        self.show()

    @pyqtSlot(int)
    def update_speed(self, speed):
        self.speed_label.setText('Speed: {} km/h'.format(speed))

    @pyqtSlot(str)
    def update_mode(self, mode):
        self.mode_label.setText('Mode: {}'.format(mode))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = Data()
    dashboard = Dashboard(data)
    data.speed_changed.connect(dashboard.update_speed)
    data.mode_changed.connect(dashboard.update_mode)
    sys.exit(app.exec_())
