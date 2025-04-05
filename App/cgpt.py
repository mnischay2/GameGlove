import pygame
import serial.tools.list_ports
import serial
import sys
import os
from pynput.keyboard import Controller, Key
import time
import combo

# Initialize
keyboard = Controller()
pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameGlove Controller")
pygame.display.set_icon(pygame.image.load("assets/Images/icon.png"))

# Directories
IMAGE_DIR = "assets\\Images"
FONT_DIR = "assets\\Fonts"

# Variables
on_off = 0
circle_button_radius = 25
on_off_button_radius = 45
forward = ["", "", ""]
backward = ["", "", ""]
left = ["", "", ""]
right = ["", "", ""]
index = ["", "", ""]
little = ["", "", ""]
ser = None  # Serial connection object

# Load key combos
try:
    with open("assets/state_data.txt", "r") as file:
        data = file.read().split('\n')
        combo.seperate_key_combo(data[0], forward)
        combo.seperate_key_combo(data[1], backward)
        combo.seperate_key_combo(data[2], left)
        combo.seperate_key_combo(data[3], right)
        combo.seperate_key_combo(data[4], index)
        combo.seperate_key_combo(data[5], little)
except FileNotFoundError:
    print("Error: assets/state_data.txt file not found.")

def save_data():
    combo.save_key_combo(0, forward)
    combo.save_key_combo(1, backward)
    combo.save_key_combo(2, left)
    combo.save_key_combo(3, right)
    combo.save_key_combo(4, index)
    combo.save_key_combo(5, little)

# Load image function
def load_image(filename, size=None):
    try:
        image = pygame.image.load(os.path.join(IMAGE_DIR, filename)).convert_alpha()
        return pygame.transform.scale(image, size) if size else image
    except FileNotFoundError:
        print(f"Error: {filename} not found in 'assets' directory.")
        return None

# UI Sizes & Positions
def circle_button_size(radius): return (radius * 2, radius * 2)
scan_img = load_image("scan.png", circle_button_size(circle_button_radius))
connect_img = load_image("connect.png", circle_button_size(circle_button_radius))
connected_img = load_image("connected.png", circle_button_size(circle_button_radius))
on_img = load_image("on.png", circle_button_size(on_off_button_radius))
off_img = load_image("off.png", circle_button_size(on_off_button_radius))

# Placeholder
def create_placeholder(color, radius):
    img = pygame.Surface(circle_button_size(radius), pygame.SRCALPHA)
    pygame.draw.circle(img, color, (radius, radius), radius)
    return img
if not scan_img: scan_img = create_placeholder((0, 255, 0), circle_button_radius)
if not connect_img: connect_img = create_placeholder((255, 0, 0), circle_button_radius)
if not connected_img: connected_img = create_placeholder((0, 0, 255), circle_button_radius)

# Fonts
font = pygame.font.Font(None, 27)
retropix_font = pygame.font.Font(os.path.join(FONT_DIR, "retropix.ttf"), 120)
justice_font = pygame.font.Font(os.path.join(FONT_DIR, "justice.ttf"), 25)
barbarian_font = pygame.font.Font(os.path.join(FONT_DIR, "barbarian.ttf"), 120)

# UI Element Positions
label_pos = (20, 30)
title_pos = (WIDTH // 2, 150)
scan_pos = (170, 20)
dropdown_pos = (230, 20)
connect_pos = (460, 20)
on_off_pos = (250, 250)

dropdown_width, dropdown_height = 210, 50
dropdown_open = False

# Get ports
def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports] if ports else ["No device connected"]

def is_device_connected(device):
    return device in get_serial_ports()

# Read data from ESP32 (keep connection open)
def read_esp32():
    global ser
    try:
        if ser and ser.in_waiting:
            data = str(ser.readline().decode('latin-1', 'ignore').strip())
            return data
        return ""
    except serial.SerialException as e:
        print("Serial Error:", e)
        return ""

# Press keys
def press_keys(key1, key2, key3):
    if key2 == "": key2 = key1
    if key3 == "": key3 = key1
    duration = 0.01
    keyboard.press(key1)
    keyboard.press(key2)
    keyboard.press(key3)
    time.sleep(duration)
    keyboard.release(key1)
    keyboard.release(key2)
    keyboard.release(key3)

# Circle click
def if_clicked_in_circle(mx, my, pos, r):
    return (mx - pos[0] - r)**2 + (my - pos[1] - r)**2 <= r**2

# Initial values
available_ports = get_serial_ports()
selected_device = available_ports[0] if available_ports else "No device connected"
is_connected = False

# Main loop
running = True
while running:
    data_read = read_esp32()
    screen.blit(load_image("theme.png", (WIDTH, HEIGHT)) or pygame.Surface((WIDTH, HEIGHT)), (0, 0))

    screen.blit(retropix_font.render("GameGlove", True, (255, 255, 255)), retropix_font.render("GameGlove", True, (255, 255, 255)).get_rect(center=title_pos))
    screen.blit(justice_font.render("Select Device ", True, (255, 255, 255)), label_pos)

    screen.blit(scan_img, scan_pos)
    screen.blit(connected_img if is_connected else connect_img, connect_pos)
    pygame.draw.rect(screen, (50, 50, 50), (*dropdown_pos, dropdown_width, dropdown_height), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), (*dropdown_pos, dropdown_width, dropdown_height), 2, border_radius=10)

    screen.blit(font.render(selected_device, True, (255, 255, 255)), (dropdown_pos[0] + 10, dropdown_pos[1] + 10))
    screen.blit(on_img if on_off == 1 else off_img, on_off_pos)

    if dropdown_open:
        for i, port in enumerate(available_ports):
            rect = pygame.Rect(dropdown_pos[0], dropdown_pos[1] + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
            pygame.draw.rect(screen, (70, 70, 70), rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=10)
            screen.blit(font.render(port, True, (255, 255, 255)), (rect.x + 10, rect.y + 10))

    if is_connected and not is_device_connected(selected_device):
        is_connected = False
        on_off = 0
        ser = None
        available_ports = get_serial_ports()
        selected_device = available_ports[0] if available_ports else "No device connected"

    if on_off == 1 and data_read:
        readings = data_read.split(",")
        for i in readings:
            if i == "FRONT":
                press_keys(forward[0], forward[1], forward[2])
            elif i == "BACK":
                press_keys(backward[0], backward[1], backward[2])
            elif i == "LEFT":
                press_keys(left[0], left[1], left[2])
            elif i == "RIGHT":
                press_keys(right[0], right[1], right[2])
            elif i == "INDEX":
                press_keys(index[0], index[1], index[2])
            elif i == "LITTLE":
                press_keys(little[0], little[1], little[2])
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # save_data()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if if_clicked_in_circle(mx, my, scan_pos, circle_button_radius):
                available_ports = get_serial_ports()
                selected_device = available_ports[0] if available_ports else "No device connected"

            elif if_clicked_in_circle(mx, my, connect_pos, circle_button_radius):
                if selected_device != "No device connected":
                    try:
                        ser = serial.Serial(selected_device, 9600, timeout=1)
                        is_connected = True
                    except serial.SerialException:
                        is_connected = False
                        ser = None

            elif if_clicked_in_circle(mx, my, on_off_pos, on_off_button_radius):
                if is_connected:
                    on_off = 1 if on_off == 0 else 0
                else:
                    on_off = 0

            elif dropdown_pos[0] < mx < (dropdown_pos[0] + dropdown_width) and dropdown_pos[1] < my < (dropdown_pos[1] + dropdown_height):
                dropdown_open = not dropdown_open

            if dropdown_open:
                for i, port in enumerate(available_ports):
                    option_rect = pygame.Rect(dropdown_pos[0], dropdown_pos[1] + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
                    if option_rect.collidepoint(mx, my):
                        selected_device = port
                        dropdown_open = False

    pygame.display.flip()

pygame.quit()
sys.exit()
