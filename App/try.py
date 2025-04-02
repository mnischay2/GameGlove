import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import serial
import pygame
from PIL import Image, ImageTk

# Initialize pygame for key handling
pygame.init()

# Create main window
root = tk.Tk()
root.title("GameGlove Controller")
root.geometry("900x1200")  # 3:4 aspect ratio


try:
    bg_image = Image.open("assets/theme.png").resize((900, 1200))
    # Load button images
    connect_img = ImageTk.PhotoImage(Image.open("assets/connect.png").resize((100, 100)))
    connected_img = ImageTk.PhotoImage(Image.open("assets/connected.png").resize((100, 100)))
    scan_img = ImageTk.PhotoImage(Image.open("assets/scan.png").resize((100, 100)))

    file=open('assets/state_data.txt','r')
    data=str(file.read()).split('\n')

    forward_combo= data[0]
    backward_combo =data[1]
    left_combo = data[2]
    right_combo = data[3]
    index_combo = data[4]
    forward_left_combo = data[5]
    forward_right_combo = data[6]
    backward_left_combo = data[7]
    backward_right_combo = data[8]

except FileNotFoundError:
    print("Error: Required files not found in 'assets' directory.")
    run=False

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports] if ports else ["No device connected"]

def scan_devices():
    ports = get_serial_ports()
    port_dropdown["values"] = ports
    port_var.set(ports[0])

def connect_device():
    selected_port = port_var.get()
    if selected_port and selected_port != "No device connected":
        try:
            ser = serial.Serial(selected_port, 9600, timeout=2)
            ser.close()
            connect_btn.config(image=connected_img)
        except serial.SerialException:
            connect_btn.config(image=connect_img)

# Initialize pygame for key handling
pygame.init()

# Create main window
root = tk.Tk()
root.title("GameGlove Controller")
root.geometry("900x1200")  # 3:4 aspect ratio

# Load background image
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)


# Dropdown for selecting serial port
port_var = tk.StringVar()
ports = get_serial_ports()
port_dropdown = ttk.Combobox(root, textvariable=port_var, values=ports, state='readonly')
port_dropdown.pack(pady=20)
port_var.set(ports[0])

# Scan button
scan_btn = tk.Button(root, image=scan_img, command=scan_devices, borderwidth=0)
scan_btn.pack(pady=10)

# Connect button
connect_btn = tk.Button(root, image=connect_img, command=connect_device, borderwidth=0)
connect_btn.pack(pady=20)

# Run GUI loop
root.mainloop()