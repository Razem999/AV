import serial
import time

#adruino = serial.Serial('/dev/tty/ACM0', 115200,timeouts = 5)

adruino = serial.Serial(
port = '/dev/ttyUSB0',
baudrate=9600,
bytesize =serial.EIGHTBITS,
parity = serial.PARITY_NONE,
stopbits = serial.STOPBITS_ONE,
timeout =5,
xonxoff = False,
rtscts = False,
dsrdtr = False,
writeTimeout = 2
)

while True:
    try:
        adruino.write("Successful test from Jetson AV tests|".encode())
        data = adruino.readline()
        if data:
            print(data)
        time.sleep(1)
    except Exception as e:
        print(e)
        adruino.close()


 
