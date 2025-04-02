import pygame
import serial.tools.list_ports
import serial
import sys
import os
from pynput.keyboard import Controller, Key
import time
import combo

# Initialize imp things
keyboard = Controller()
pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameGlove Controller")
pygame.display.set_icon(pygame.image.load("assets/Images/icon.png"))
# directory
IMAGE_DIR = "assets\Images"
FONT_DIR = "assets\Fonts"

#variables
on_off=0
circle_button_radius = 25
on_off_button_radius = 45


#function to load images
def load_image(filename, size=None):
    try:
        image = pygame.image.load(os.path.join(IMAGE_DIR, filename)).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except FileNotFoundError:
        print(f"Error: {filename} not found in 'assets' directory.")
        return None

# Load Background Image
bg_image = load_image("theme.png", (WIDTH, HEIGHT))

def circle_button_size(radius):
    return (radius * 2, radius * 2)

scan_img = load_image("scan.png", circle_button_size(circle_button_radius))
connect_img = load_image("connect.png", circle_button_size(circle_button_radius))
connected_img = load_image("connected.png", circle_button_size(circle_button_radius))
on_img = load_image("on.png", circle_button_size(on_off_button_radius))
off_img = load_image("off.png", circle_button_size(on_off_button_radius))
# Placeholder images if missing
def create_placeholder(color, radius):
    img = pygame.Surface(circle_button_size(radius), pygame.SRCALPHA)
    pygame.draw.circle(img, color, (radius, radius), radius)
    return img

if not scan_img:
    scan_img = create_placeholder((0, 255, 0), circle_button_radius)
if not connect_img:
    connect_img = create_placeholder((255, 0, 0), circle_button_radius)
if not connected_img:
    connected_img = create_placeholder((0, 0, 255), circle_button_radius)

# UI Element Positions
label_pos = (20, 30)
title_pos = (WIDTH // 2, 150)
scan_pos = (170, 20)
dropdown_pos = (230, 20)
connect_pos = (460, 20)
on_off_pos = (250, 250)

# Device Dropdown settings
dropdown_width = 210  
dropdown_height = 50
dropdown_open = False

# Fonts
font = pygame.font.Font(None, 27)
retropix_font = pygame.font.Font(os.path.join(FONT_DIR, "retropix.ttf"), 120)
justice_font = pygame.font.Font(os.path.join(FONT_DIR, "justice.ttf"), 25)
barbarian_font = pygame.font.Font(os.path.join(FONT_DIR, "barbarian.ttf"), 120)

# Function to get available serial ports
def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports] if ports else ["No device connected"]

# Function to check if a device is connected
def is_device_connected(device):
    return device in get_serial_ports()

# Function to check if a click is inside a circle
def if_clicked_in_circle(mouse_x, mouse_y, circle_pos, radius):
    return (mouse_x - circle_pos[0] - radius) ** 2 + (mouse_y - circle_pos[1] - radius) ** 2 <= radius ** 2

# Function to press keys
def press_keys(key1, key2, key3):
    duration = 0.01
    keyboard.press(key1)
    keyboard.press(key2)
    keyboard.press(key3)
    time.sleep(duration)  # Hold keys for the duration
    keyboard.release(key1)
    keyboard.release(key2)
    keyboard.release(key3)
    
# Initial Device List & Selection
available_ports = get_serial_ports()
selected_device = available_ports[0] if available_ports else "No device connected"
is_connected = False

# Main Loop
running = True
while running:
    screen.blit(bg_image, (0, 0)) if bg_image else screen.fill((0, 91, 255))

    title_text = retropix_font.render("GameGlove", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=title_pos)
    screen.blit(title_text, title_rect)

    label_text = justice_font.render("Select Device ", True, (255, 255, 255))
    screen.blit(label_text, label_pos)

    screen.blit(scan_img, scan_pos)
    screen.blit(connect_img if not is_connected else connected_img, connect_pos)

    pygame.draw.rect(screen, (50, 50, 50), (*dropdown_pos, dropdown_width, dropdown_height), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), (*dropdown_pos, dropdown_width, dropdown_height), 2, border_radius=10)

    device_text = font.render(selected_device, True, (255, 255, 255))
    screen.blit(device_text, (dropdown_pos[0] + 10, dropdown_pos[1] + 10))

    screen.blit(on_img  if on_off==1 else off_img, on_off_pos)

    if dropdown_open:
        for i, port in enumerate(available_ports):
            option_rect = pygame.Rect(dropdown_pos[0], dropdown_pos[1] + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
            pygame.draw.rect(screen, (70, 70, 70), option_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), option_rect, 2, border_radius=10)
            option_text = font.render(port, True, (255, 255, 255))
            screen.blit(option_text, (option_rect.x + 10, option_rect.y + 10))

    if is_connected and not is_device_connected(selected_device):
        is_connected = False
        on_off = 0
        available_ports = get_serial_ports()
        selected_device = available_ports[0] if available_ports else "No device connected"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if if_clicked_in_circle(mouse_x, mouse_y, scan_pos, circle_button_radius):
                available_ports = get_serial_ports()
                selected_device = available_ports[0] if available_ports else "No device connected"

            elif if_clicked_in_circle(mouse_x, mouse_y, connect_pos, circle_button_radius):
                if selected_device != "No device connected":
                    try:
                        ser = serial.Serial(selected_device, 9600, timeout=2)
                        ser.close()
                        is_connected = True
                        available_ports = get_serial_ports()
                        selected_device = available_ports[0] if available_ports else "No device connected"
                    except serial.SerialException:
                        is_connected = False

            elif if_clicked_in_circle(mouse_x, mouse_y, on_off_pos, on_off_button_radius):
                if is_connected:
                    if on_off == 0:
                        on_off = 1
                    else:
                        on_off = 0
                else:
                    on_off = 0

            elif dropdown_pos[0] < mouse_x < (dropdown_pos[0] + dropdown_width) and dropdown_pos[1] < mouse_y < (dropdown_pos[1] + dropdown_height):
                dropdown_open = not dropdown_open

            if dropdown_open:
                for i, port in enumerate(available_ports):
                    option_rect = pygame.Rect(dropdown_pos[0], dropdown_pos[1] + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        selected_device = port
                        dropdown_open = False

    pygame.display.flip()

pygame.quit()
sys.exit()

