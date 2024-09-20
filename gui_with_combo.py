import serial.tools.list_ports
import serial  # sudo pip install pyserial should work
import pickle
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Load the model
with open('model.pkl', 'rb') as f:
    reg_model = pickle.load(f)

# Baud rate (fixed)
baud_rate = 9600

# Create the main window
root = tk.Tk()
root.title("Serial Data with Predictions")

# Function to list available serial ports


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


# Create UI elements for port selection
port_label = tk.Label(root, text="Select Serial Port:")
port_label.grid(row=0, column=0, padx=10, pady=10)

# Create a combobox for selecting the serial port
port_combobox = ttk.Combobox(
    root, values=list_serial_ports(), state="readonly")
port_combobox.grid(row=0, column=1, padx=10, pady=10)

# Button to refresh the list of ports


def refresh_ports():
    port_combobox['values'] = list_serial_ports()


refresh_button = tk.Button(root, text="Refresh Ports", command=refresh_ports)
refresh_button.grid(row=0, column=2, padx=10, pady=10)

# Create the treeview to display the table
tree = ttk.Treeview(root)
tree['columns'] = ('r', 's', 't', 'u', 'v', 'w', 'predicted')

# Define the column headings
for col in tree['columns']:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Set the initial layout of the table
tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Global serial object
ser = None

# Function to append rows to the table


def append_to_table(data_row, predicted_value):
    tree.insert("", "end", values=data_row + [predicted_value])

# Function to start reading serial data


def start_reading():
    global ser
    selected_port = port_combobox.get()

    if not selected_port:
        messagebox.showerror("Error", "Please select a serial port!")
        return

    try:
        # Open the serial port
        ser = serial.Serial(selected_port, baud_rate)
        # Start reading the data
        read_serial_data()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open serial port: {e}")

# Function to read from the serial port and update the UI


def read_serial_data():
    global ser
    if ser:
        try:
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
        except Exception as e:
            messagebox.showerror("Error", f"Error reading serial data: {e}")

    # Call the function again after a short delay
    root.after(1000, read_serial_data)  # Repeat every 1000 ms


# Button to start reading data
start_button = tk.Button(root, text="Start", command=start_reading)
start_button.grid(row=0, column=3, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
