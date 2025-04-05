from pynput.keyboard import Key

def seperate_key_combo(input_string, output_list):
    parts = input_string.strip().split(",")
    for i in range(3):
        output_list[i] = convert_to_key(parts[i]) if i < len(parts) else ""

def combine_key_combo(key1, key2, key3):
    return f"{key1},{key2},{key3}"

def save_key_combo(line_number, key_combo):
    with open('assets/state_data.txt', 'r') as file:
        lines = file.readlines()
    
    if line_number < 0 or line_number >= len(lines):
        print("Error: Line number out of range.")
        return
    
    lines[line_number] = key_combo + '\n'
    
    with open('assets/state_data.txt', 'w') as file:
        file.writelines(lines)

def convert_to_key(key_str):
    """
    Converts a string to a pynput-compatible key. 
    For alphanumeric, returns the character.
    For special keys, returns Key.<keyname>
    """
    if key_str == "":
        return ""
    
    special_keys = {
        'space': Key.space,
        'enter': Key.enter,
        'shift': Key.shift,
        'ctrl': Key.ctrl,
        'alt': Key.alt,
        'tab': Key.tab,
        'esc': Key.esc,
        'backspace': Key.backspace,
        'delete': Key.delete,
        'caps_lock': Key.caps_lock,
        'cmd': Key.cmd,
        'home': Key.home,
        'end': Key.end,
        'page_up': Key.page_up,
        'page_down': Key.page_down,
        'up': Key.up,
        'down': Key.down,
        'left': Key.left,
        'right': Key.right,
        'f1': Key.f1,
        'f2': Key.f2,
        'f3': Key.f3,
        'f4': Key.f4,
        'f5': Key.f5,
        'f6': Key.f6,
        'f7': Key.f7,
        'f8': Key.f8,
        'f9': Key.f9,
        'f10': Key.f10,
        'f11': Key.f11,
        'f12': Key.f12
    }

    key_str_lower = key_str.lower().strip()
    return special_keys.get(key_str_lower, key_str_lower)  # fall back to alphanum
