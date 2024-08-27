import serial.tools.list_ports
import serial  # sudo pip install pyserial should work

ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

serial_port = '/dev/ttyACM0'
baud_rate = 9600  # In arduino, Serial.begin(baud_rate)
ser = serial.Serial(serial_port, baud_rate)
while True:
    line = ser.readline()
    # ser.readline returns a binary, convert to string
    line = line.decode("utf-8")
    print(line)
