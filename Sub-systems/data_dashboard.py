import can
import time
import datetime
from datetime import datetime
import sys
from PyQt5.QtCore import Qt, QTimer,QTime
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QWidget,QVBoxLayout

# class DigitalClock(QLabel):
#     def __init__(self):
#         super().__init__()

#         #set font and alignment
#         font= QFont("Arial",24,QFont.Bold)
#         self.setFont(font)
#         self.setAlignment(Qt.AlignCenter)
        

#         #timer to update clock everysecond
#         timer =QTimer(self)
#         timer.timeout.connect(self.update_time)
#         timer.start(1000)

#         self.update_time()

#     def update_time(self):
#         current_time = QTime.currentTime()
#         time_string = current_time.toString('hh:mm:ss')
#         self.setText(time_string)

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the CAN bus and set up message filters
        # self.bus = can.Bus(bustype='socketcan', channel='can0')
        
        # self.bus.set_filters([
        #     {"can_id": 0x4, "can_mask": 0x7FF,"extended": False},
        # ])

        #Change background
        self.setStyleSheet("background-color: cyan")

        # Create the widgets for the dashboard
        self.title_label = QLabel("Group 69: CESC") #Autonomous Vehicle Central Embedded System and Controller
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 18,QFont.Bold))
        self.title_label.setStyleSheet("color:red")
        

        self.mode_label = QLabel("Mode: MANUAL")
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.mode_label.setFont(QFont("Arial", 18))
        
        self.speed_label = QLabel("Speed: 0 km/h")
        self.speed_label.setAlignment(Qt.AlignCenter)
        self.speed_label.setFont(QFont("Arial", 18))
        
        self.object_label = QLabel("Object Detected: NO")
        self.object_label.setAlignment(Qt.AlignCenter)
        self.object_label.setFont(QFont("Arial", 18))

        self.killSwitch_label = QLabel("KILL SWITCH: DE-ACTIVATED")
        self.killSwitch_label.setAlignment(Qt.AlignCenter)
        self.killSwitch_label.setFont(QFont("Arial", 18))

        self.time_label = QLabel("Time: N/A")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("Arial", 18))

        #self.clock=DigitalClock()

        



        # Create a grid layout for the widgets
        grid = QGridLayout()
        grid.addWidget(self.title_label, 0,1)
        grid.addWidget(self.mode_label, 1, 0)
        grid.addWidget(self.speed_label, 1, 1)
        grid.addWidget(self.object_label, 1, 2)
        grid.addWidget(self.killSwitch_label, 2, 2)
        grid.addWidget(self.time_label, 2, 1)
        #grid.addWidget(self.clock, 1, 2)

        # Create a central widget and set the grid layout as its layout
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        #timer that reads data from canbus every 100ms
        self.timer =QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

        
           

        

    def update_data(self):
        #while True:
        # Read the data from the CAN bus
        bus = can.Bus(channel='can0', bustype='socketcan')
        bus.set_filters([
            {"can_id": 0x004, "can_mask": 0x7FF, "extended": False},
            {"can_id": 0x005, "can_mask": 0x7FF, "extended": False},
            {"can_id": 0x006, "can_mask": 0x7FF, "extended": False},
            {"can_id": 0x007, "can_mask": 0x7FF, "extended": False}
        ])

        message = bus.recv(1.0)
        
        message_dict ={
            'id': hex(message.arbitration_id),
            'data':message.data,
            #'timestamp': datetime.datetime.fromtimestamp(message.timestamp),
            'dlc': message.dlc
        }

        print("data", message_dict['id'])
        print("data", message_dict['data'][7])
        #print(f"message data at 0: {message_dict['data'][0]}")

        #---------- MODE OF CAR -------------
        if message_dict['id'] == '0x6'or message_dict['id']== '0x4':
            #test1=message_dict['data'][10]
            #print(f"message data at 0: {message_dict['data'][0]}")
            #print(test1)
            #mode manual or auto
            if message_dict['data'][7] == 1:
                mode_detected = "AUTOMATIC"
                self.mode_label.setText(f"Mode: {mode_detected}")
                #speed = message_dict['data'][0]
                # self.speed_label.setText(f"Speed: {speed} km/h")
                
            else:
                mode_detected = "MANUAL"
                self.mode_label.setText(f"Mode: {mode_detected}")
                # speed = message_dict['data'][0]
                # self.speed_label.setText(f"Speed: {speed} km/h")
        
        #--------- SPEED -------------
        if message_dict['id'] == '0x4':
            speed = message_dict['data'][0]
            self.speed_label.setText(f"Speed: {speed} km/h")
      
        

        #------------OBJECT DETECTED ------------------
        if message_dict['id'] == '0x5':
            if message_dict['data'][5] == 1:
                object_detected = "YES"
                print("yes")
            else:
                object_detected = "NO"
                print('no')
            self.object_label.setText(f"Object Detected: {object_detected}")
        

        #----------KILL SWITCH -------------
        if message_dict['id'] == '0x7':
            if message_dict['data'][6] == 1:
                kill_switch = "ACTIVATED"
                #print("yes")
            else:
                kill_switch = "DE-ACTIVATED"
                #print('no')
            self.killSwitch_label.setText(f"KILL-SWITCH: {kill_switch}")
        

        #update the time with curr values
        now =datetime.now()
        current_time = now.strftime("%H:%M:%S")
        test1=int(message_dict['data'][0])
        self.time_label.setText(f"Time: {current_time}")
        # test1=int(message_dict['data'][0])
        # #print(f"message data at 0: {message_dict['data'][0]}")
        # #print(test1)
        # self.mode_label.setText(f"Mode: {test1}")


        #wait before listening for next message
        #time.sleep(0.1)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
