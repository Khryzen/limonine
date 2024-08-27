import serial.tools.list_ports
import serial  # sudo pip install pyserial should work

import pickle
import numpy as np
import pandas as pd

with open('model.pkl', 'rb') as f:
  reg_model = pickle.load(f)

ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

serial_port = '/dev/ttyACM0'
baud_rate = 9600  # In arduino, Serial.begin(baud_rate)
ser = serial.Serial(serial_port, baud_rate)
while True:
    line = ser.readline()
    # ser.readline returns a binary, convert to string
    line = line.decode("utf-8").strip()
    print(line)

    # Split the line into a list of strings based on commas
    str_values = line.split(',')

    # Convert the list of strings to a list of floats
    float_values = [float(value) for value in str_values]

    # Convert the list of floats to a NumPy array
    row = np.array(float_values)

    # row = np.array([407.65, 50.07, 91.33, 53.93, 34.34, 19.08])
    feature_names = ['r', 's', 't', 'u', 'v', 'w']

    X_new = pd.DataFrame([row], columns=feature_names)
    pred = reg_model.predict(X_new)
    print(f'Predicted Value: {pred}')
    # print(pred)




