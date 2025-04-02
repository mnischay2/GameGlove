import pygame
import serial.tools.list_ports
import serial
import sys
import os
import time

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameGlove Controller")

# directory
IMAGE_DIR = "assets\Images"
FONT_DIR = "assets\Fonts"

#files
state_file_name= 'state_data.txt'
info_file_name = 'info.txt'

def load_file(DIR, filename):
    try:
        file=open('assets/state_data.txt','r')
        return file
    except FileNotFoundError:
        print(f"Error: {filename} not found in {DIR} directory.")
        return None

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

#circle button setting 
circle_button_radius=25
def circle_button_size(radius):
    return (radius * 2, radius * 2)

scan_img = load_image("scan.png", circle_button_size(circle_button_radius))
connect_img = load_image("connect.png", circle_button_size(circle_button_radius))
connected_img = load_image("connected.png", circle_button_size(circle_button_radius))

state_file = load_file(IMAGE_DIR, state_file_name)
info_file = load_file(IMAGE_DIR, info_file_name)

# If any image is missing, create a placeholder circle
def create_placeholder(color, radius):
    img = pygame.Surface(circle_button_size(radius), pygame.SRCALPHA)
    pygame.draw.circle(img, color, (radius, radius), radius)
    return img

if not scan_img:
    scan_img = create_placeholder((0, 255, 0), circle_button_radius)  # Green for scan
if not connect_img:
    connect_img = create_placeholder((255, 0, 0), circle_button_radius)  # Red for connect
if not connected_img:
    connected_img = create_placeholder((0, 0, 255), circle_button_radius)  # Blue for connected

# UI Element Positions
label_pos = (20, 30)
title_pos = (WIDTH // 2, 150)
scan_pos = (170, 20)
dropdown_pos = (230, 20)
connect_pos = (460, 20)

# Dropdown settings
dropdown_width = 210  
dropdown_height = 50
dropdown_open = False

# Fonts
font = pygame.font.Font(None, 25)  # Default font
retropix_font = pygame.font.Font(os.path.join(FONT_DIR, "retropix.ttf"), 120)
justice_font = pygame.font.Font(os.path.join(FONT_DIR, "justice.ttf"), 25)

# Get Available Serial Ports
def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports] if ports else ["No device connected"]

# Check if device is still connected
def is_device_connected(device):
    return device in get_serial_ports()

def if_clicked_in_circle(mouse_x, mouse_y, circle_pos, radius):
    if (mouse_x - circle_pos[0] - radius) ** 2 + (mouse_y - circle_pos[1] - radius) ** 2 <= radius ** 2:
        return True
    else: 
        return False

# Initial Device List & Selection
available_ports = get_serial_ports()
selected_device = available_ports[0] if available_ports else "No device connected"
is_connected = False

# Main Loop
running = True
while running:
    screen.blit(bg_image, (0, 0)) if bg_image else screen.fill((0, 91, 255))  # Fallback background

    # Draw GameGlove Title
    title_text = retropix_font.render("GameGlove", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=title_pos)
    screen.blit(title_text, title_rect)

    # Draw UI Elements
    label_text = justice_font.render("Select Device ", True, (255, 255, 255))
    screen.blit(label_text, label_pos)
    

    screen.blit(scan_img, scan_pos)
    screen.blit(connect_img if not is_connected else connected_img, connect_pos)

    pygame.draw.rect(screen, (50, 50, 50), (*dropdown_pos, dropdown_width, dropdown_height), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), (*dropdown_pos, dropdown_width, dropdown_height), 2, border_radius=10)

    device_text = font.render(selected_device, True, (255, 255, 255))
    screen.blit(device_text, (dropdown_pos[0] + 10, dropdown_pos[1] + 10))

    # Draw Dropdown Options
    if dropdown_open:
        for i, port in enumerate(available_ports):
            option_rect = pygame.Rect(dropdown_pos[0], dropdown_pos[1] + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
            pygame.draw.rect(screen, (70, 70, 70), option_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), option_rect, 2, border_radius=10)
            option_text = font.render(port, True, (255, 255, 255))
            screen.blit(option_text, (option_rect.x + 10, option_rect.y + 10))

    # Periodically check if the connected device is still available
    if is_connected and not is_device_connected(selected_device):
        is_connected = False

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Scan Button Clicked
            if if_clicked_in_circle(mouse_x, mouse_y, scan_pos, circle_button_radius):
                available_ports = get_serial_ports()
                selected_device = available_ports[0] if available_ports else "No device connected"

            # Connect Button Clicked
            elif if_clicked_in_circle(mouse_x, mouse_y, connect_pos, circle_button_radius):
                if selected_device != "No device connected":
                    try:
                        ser = serial.Serial(selected_device, 9600, timeout=2)
                        ser.close()
                        is_connected = True
                    except serial.SerialException:
                        is_connected = False

            # Dropdown Clicked
            elif dropdown_pos[0] < mouse_x < (dropdown_pos[0] + dropdown_width) and dropdown_pos[1] < mouse_y < (dropdown_pos[1] + dropdown_height):
                dropdown_open = not dropdown_open

            # Selecting an Option
            if dropdown_open:
                for i, port in enumerate(available_ports):
                    option_rect = pygame.Rect(dropdown_pos[0], dropdown_pos[1] + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        selected_device = port
                        dropdown_open = False

    pygame.display.flip()  # Update Screen
# Quit Pygame
pygame.quit()
sys.exit()
