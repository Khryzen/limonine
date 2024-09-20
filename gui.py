import serial.tools.list_ports
import serial  # sudo pip install pyserial should work
import pickle
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk

# Load the model
with open('model.pkl', 'rb') as f:
    reg_model = pickle.load(f)

# Serial setup
serial_port = '/dev/ttyACM0'
baud_rate = 9600  # In Arduino, Serial.begin(baud_rate)
ser = serial.Serial(serial_port, baud_rate)

# Create the main window
root = tk.Tk()
root.title("Serial Data with Predictions")

# Create the treeview to display the table
tree = ttk.Treeview(root)
tree['columns'] = ('r', 's', 't', 'u', 'v', 'w', 'predicted')

# Define the column headings
for col in tree['columns']:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Set the initial layout of the table
tree.grid(row=0, column=0, padx=10, pady=10)

# A function to append rows to the table
def append_to_table(data_row, predicted_value):
    tree.insert("", "end", values=data_row + [predicted_value])

# Function to read from the serial port and update the UI
def read_serial_data():
    line = ser.readline()
    line = line.decode("utf-8").strip()

    # Split the line into a list of strings based on commas
    str_values = line.split(',')

    # Convert the list of strings to a list of floats
    float_values = [float(value) for value in str_values]

    # Convert the list of floats to a NumPy array
    row = np.array(float_values)

    # Create a DataFrame for prediction
    feature_names = ['r', 's', 't', 'u', 'v', 'w']
    X_new = pd.DataFrame([row], columns=feature_names)

    # Predict
    pred = reg_model.predict(X_new)[0]

    # Append the new data and prediction to the table
    append_to_table(float_values, pred)

    # Call the function again after a short delay
    root.after(1000, read_serial_data)  # Repeat every 1000 ms

# Start reading serial data
root.after(1000, read_serial_data)

# Run the Tkinter event loop
root.mainloop()
