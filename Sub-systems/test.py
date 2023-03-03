#to open designer /usr/lib/aarch64-linux-gnu/qt5/bin/designer
import sys
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("AV CESC Michael test")

    win.show()
    sys.exit(app.exe_())

window()

# from PyQt5.QtWidgets import QApplication, QWidget

# import sys

# app = QApplication(sys.argv)
# window = QWidget()
# window.show()

# app.exec()
