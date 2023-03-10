import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QWidget

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the CAN bus and set up message filters
        self.bus = can.interface.Bus(bustype='socketcan', channel='can0')
        self.bus.set_filters([
            {"can_id": 0x100, "can_mask": 0x7FF},
            {"can_id": 0x101, "can_mask": 0x7FF},
            {"can_id": 0x102, "can_mask": 0x7FF},
        ])

        # Create the widgets for the dashboard
        self.mode_label = QLabel("Mode: N/A")
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.mode_label.setFont(QFont("Arial", 18))
        
        self.speed_label = QLabel("Speed: N/A")
        self.speed_label.setAlignment(Qt.AlignCenter)
        self.speed_label.setFont(QFont("Arial", 18))
        
        self.object_label = QLabel("Object Detected: N/A")
        self.object_label.setAlignment(Qt.AlignCenter)
        self.object_label.setFont(QFont("Arial", 18))

        # Create a grid layout for the widgets
        grid = QGridLayout()
        grid.addWidget(self.mode_label, 0, 0)
        grid.addWidget(self.speed_label, 0, 1)
        grid.addWidget(self.object_label, 0, 2)

        # Create a central widget and set the grid layout as its layout
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # Set up a timer to read data from the CAN bus every 100ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def update_data(self):
        # Read the data from the CAN bus
        messages = self.bus.recv(10)
        for message in messages:
            if message.arbitration_id == 0x100:
                self.mode_label.setText(f"Mode: {message.data[0]}")
            elif message.arbitration_id == 0x101:
                speed = (message.data[0] << 8) | message.data[1]
                self.speed_label.setText(f"Speed: {speed} km/h")
            elif message.arbitration_id == 0x102:
                object_detected = message.data[0]
                self.object_label.setText(f"Object Detected: {object_detected}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
