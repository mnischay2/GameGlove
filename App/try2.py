import pygame
import serial.tools.list_ports
import serial
import sys
import os
import time

# Initialize Pygame
pygame.init()

# Window Settings
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameGlove Controller")

# Assets directory
ASSETS_DIR = "assets"

# Function to load images safely
def load_image(filename, size=None):
    try:
        image = pygame.image.load(os.path.join(ASSETS_DIR, filename)).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except FileNotFoundError:
        print(f"Error: {filename} not found in 'assets' directory.")
        return None

# Load Background Image
bg_image = load_image("theme.png", (WIDTH, HEIGHT))

# Load Button Images
BUTTON_RADIUS = 25  # Circular Button Radius
BUTTON_SIZE = (BUTTON_RADIUS * 2, BUTTON_RADIUS * 2)

scan_img = load_image("scan.png", BUTTON_SIZE)
connect_img = load_image("connect.png", BUTTON_SIZE)
connected_img = load_image("connected.png", BUTTON_SIZE)

# If any image is missing, create a placeholder circle
def create_placeholder(color):
    img = pygame.Surface(BUTTON_SIZE, pygame.SRCALPHA)
    pygame.draw.circle(img, color, (BUTTON_RADIUS, BUTTON_RADIUS), BUTTON_RADIUS)
    return img

if not scan_img:
    scan_img = create_placeholder((0, 255, 0))  # Green for scan
if not connect_img:
    connect_img = create_placeholder((255, 0, 0))  # Red for connect
if not connected_img:
    connected_img = create_placeholder((0, 0, 255))  # Blue for connected

# Button Positions
scan_pos = (WIDTH // 2 - BUTTON_RADIUS, 300)
connect_pos = (WIDTH // 2 - BUTTON_RADIUS, 500)

# Dropdown Position and Size
dropdown_width = 250  # Increased width to prevent text leakage
dropdown_height = 50
dropdown_pos = (WIDTH // 2 - dropdown_width // 2, 400)
dropdown_open = False

# Font
font = pygame.font.Font(None, 25)  # Reduced font size

# Function to check if a click is within a circular button
def is_within_circle(pos, button_pos, radius):
    return (pos[0] - (button_pos[0] + radius))**2 + (pos[1] - (button_pos[1] + radius))**2 <= radius**2

# Get Available Serial Ports
def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports] if ports else ["No device connected"]

# Check if device is still connected
def is_device_connected(device):
    return device in get_serial_ports()

# Initial Device List & Selection
available_ports = get_serial_ports()
selected_device = available_ports[0] if available_ports else "No device connected"
is_connected = False

# Main Loop
running = True
while running:
    screen.blit(bg_image, (0, 0)) if bg_image else screen.fill((0, 91 , 255))  # Fallback background

    # Draw Buttons
    screen.blit(scan_img, scan_pos)
    screen.blit(connect_img if not is_connected else connected_img, connect_pos)

    # Draw Dropdown Box
    pygame.draw.rect(screen, (50, 50, 50), (*dropdown_pos, dropdown_width, dropdown_height), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), (*dropdown_pos, dropdown_width, dropdown_height), 2, border_radius=10)

    # Display Selected Device (Truncate long names)

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
            if is_within_circle((mouse_x, mouse_y), scan_pos, BUTTON_RADIUS):
                available_ports = get_serial_ports()
                selected_device = available_ports[0] if available_ports else "No device connected"

            # Connect Button Clicked
            elif is_within_circle((mouse_x, mouse_y), connect_pos, BUTTON_RADIUS):
                if selected_device != "No device connected":
                    try:
                        ser = serial.Serial(selected_device, 9600, timeout=2)
                        ser.close()
                        is_connected = True
                    except serial.SerialException:
                        is_connected = False

            # Dropdown Clicked
            elif dropdown_pos[0] < mouse_x < dropdown_pos[0] + dropdown_width and dropdown_pos[1] < mouse_y < dropdown_pos[1] + dropdown_height:
                dropdown_open = not dropdown_open

            # Selecting an Option
            if dropdown_open:
                for i, port in enumerate(available_ports):
                    option_rect = pygame.Rect(dropdown_pos[0], dropdown_pos[1] + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        selected_device = port
                        dropdown_open = False

    pygame.display.flip()  # Update Screen    time.sleep(0.5)  # Reduce CPU usage

# Quit Pygame
pygame.quit()
sys.exit()
