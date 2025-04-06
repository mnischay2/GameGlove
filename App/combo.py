def seperate_key_combo(input_string, output_list):
    parts = input_string.strip().split(",")
    for i in range(3):
        output_list[i] = parts[i].strip() if i < len(parts) else ""

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
