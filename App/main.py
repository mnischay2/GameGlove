import pygame 
import serial.tools.list_ports
import serial
import sys
import os
import keyboard  # NEW: Using keyboard instead of pynput
import time
import combo

# Initialize
pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameGlove Controller")
pygame.display.set_icon(pygame.image.load("assets/Images/icon.png"))

# Directories
IMAGE_DIR = "assets\Images"
FONT_DIR = "assets\Fonts"

# VARIABLES
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
dropdown_open = False
editing_key = None

# UI Element Positions
label_pos = (20, 25)
title_pos = (WIDTH // 2, 200)
scan_pos = (190, 20)
dropdown_pos = (250, 20)
connect_pos = (480, 20)
on_off_pos = (250, 260)
dropdown_width, dropdown_height = 210, 50

LONG_PRESS_THRESHOLD = 0.2
gesture_state = {
    "FRONT": {"active": False, "start_time": 0},
    "BACK": {"active": False, "start_time": 0},
    "LEFT": {"active": False, "start_time": 0},
    "RIGHT": {"active": False, "start_time": 0},
    "INDEX": {"active": False, "start_time": 0},
    "LITTLE": {"active": False, "start_time": 0},
}

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

# FUNCTIONS
def save_data():
    combo.save_key_combo(0, ','.join(forward))
    combo.save_key_combo(1, ','.join(backward))
    combo.save_key_combo(2, ','.join(left))
    combo.save_key_combo(3, ','.join(right))
    combo.save_key_combo(4, ','.join(index))
    combo.save_key_combo(5, ','.join(little))

def load_image(filename, size=None):
    try:
        image = pygame.image.load(os.path.join(IMAGE_DIR, filename)).convert_alpha()
        return pygame.transform.scale(image, size) if size else image
    except FileNotFoundError:
        print(f"Error: {filename} not found in 'assets' directory.")
        return None

def if_clicked_in_circle(mouse_x, mouse_y, circle_pos, radius):
    return (mouse_x - circle_pos[0] - radius) ** 2 + (mouse_y - circle_pos[1] - radius) ** 2 <= radius ** 2

def get_keys_for_gesture(gesture):
    return {
        "FRONT": forward,
        "BACK": backward,
        "LEFT": left,
        "RIGHT": right,
        "INDEX": index,
        "LITTLE": little,
    }.get(gesture, ["", "", ""])

# UI Sizes & Positions
def circle_button_size(radius): return (radius * 2, radius * 2)
scan_img = load_image("scan.png", circle_button_size(circle_button_radius))
connect_img = load_image("connect.png", circle_button_size(circle_button_radius))
connected_img = load_image("connected.png", circle_button_size(circle_button_radius))
on_img = load_image("on.png", circle_button_size(on_off_button_radius))
off_img = load_image("off.png", circle_button_size(on_off_button_radius))
edit_img = load_image("edit.png", (20, 20))

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
orbitron_font = pygame.font.Font(os.path.join(FONT_DIR, "orbitron.ttf"), 120)
title_font = pygame.font.Font(os.path.join(FONT_DIR, "justice.ttf"), 120)
body_font = pygame.font.Font(os.path.join(FONT_DIR, "playfair.ttf"), 25)

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports] if ports else ["No device connected"]

def is_device_connected(device):
    return device in get_serial_ports()

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

# Initial values
available_ports = get_serial_ports()
selected_device = available_ports[0] if available_ports else "No device connected"
is_connected = False

def draw_gesture_mappings():
    global editing_key
    start_y = 450
    spacing = 45
    label_x = 40
    key_start_x = 200
    font_size = 25
    header_font_size = 28
    box_width = 80
    box_height = 30
    box_color = (255, 255, 255)
    text_color = (0, 0, 0)
    border_radius = 6
    gesture_font = pygame.font.Font(None, font_size)
    header_font = pygame.font.Font(None, header_font_size)

    gestures = ["FRONT", "BACK", "LEFT", "RIGHT", "INDEX", "LITTLE"]
    gesture_data = [forward, backward, left, right, index, little]

    gestures_header = header_font.render("GESTURES", True, (255, 255, 255))
    keys_header = header_font.render("KEYS", True, (255, 255, 255))
    screen.blit(gestures_header, (label_x, start_y - 40))
    screen.blit(keys_header, (key_start_x, start_y - 40))

    for i, gesture in enumerate(gestures):
        y = start_y + i * spacing
        label = gesture_font.render(gesture, True, (255, 255, 255))
        screen.blit(label, (label_x, y))
        keys = gesture_data[i]
        for j in range(3):
            box_x = key_start_x + j * (box_width + 40)
            box_rect = pygame.Rect(box_x, y - 5, box_width, box_height)
            pygame.draw.rect(screen, box_color, box_rect, border_radius=6)
            key_text = gesture_font.render(keys[j] if keys[j] else "-", True, text_color)
            text_rect = key_text.get_rect(center=box_rect.center)
            screen.blit(key_text, text_rect)
            if edit_img:
                icon_rect = edit_img.get_rect(topleft=(box_x + box_width + 5, y))
                screen.blit(edit_img, icon_rect.topleft)
                if pygame.mouse.get_pressed()[0] and icon_rect.collidepoint(pygame.mouse.get_pos()):
                    editing_key = (i, j)

# Main loop
running = True
while running:
    data_read = read_esp32()
    screen.blit(load_image("theme.png", (WIDTH, HEIGHT)) or pygame.Surface((WIDTH, HEIGHT)), (0, 0))
    title_text = title_font.render("GameGlove", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=title_pos)
    screen.blit(title_text, title_rect)
    label_text = body_font.render("Select Device ", True, (255, 255, 255))
    screen.blit(label_text, label_pos)
    screen.blit(scan_img, scan_pos)
    screen.blit(connect_img if not is_connected else connected_img, connect_pos)
    pygame.draw.rect(screen, (50, 50, 50), (*dropdown_pos, dropdown_width, dropdown_height), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), (*dropdown_pos, dropdown_width, dropdown_height), 2, border_radius=10)
    device_text = font.render(selected_device, True, (255, 255, 255))
    screen.blit(device_text, (dropdown_pos[0] + 10, dropdown_pos[1] + 10))
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
        current_time = time.time()
        active_gestures = set(readings)

        for gesture in gesture_state:
            is_active = gesture in active_gestures
            was_active = gesture_state[gesture]["active"]

            if is_active and not was_active:
                gesture_state[gesture]["active"] = True
                gesture_state[gesture]["start_time"] = current_time
                keys = get_keys_for_gesture(gesture)
                for k in keys:
                    if k: keyboard.press(k)
            elif not is_active and was_active:
                gesture_state[gesture]["active"] = False
                duration = current_time - gesture_state[gesture]["start_time"]
                keys = get_keys_for_gesture(gesture)
                for k in keys:
                    if k: keyboard.release(k)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
        elif event.type == pygame.KEYDOWN and editing_key:
            i, j = editing_key
            gesture_lists = [forward, backward, left, right, index, little]
            key_name = pygame.key.name(event.key)
            gesture_lists[i][j] = key_name
            save_data()
            editing_key = None

    draw_gesture_mappings()
    pygame.display.flip()

pygame.quit()
sys.exit()
