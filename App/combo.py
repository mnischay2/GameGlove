def seperate_key_combo(input_string,output_string):
    i=0
    for part in input_string.split(','):
        output_string [i]=part
        i+=1

def combine_key_combo(key1,key2,key3):
    return key1 + ',' +key2 +',' + key3

def save_key_combo(line_number, key_combo):
   
        with open('assets/state_data.txt', 'r') as file:
            lines = file.readlines()
        
        if line_number < 0 or line_number >= len(lines):
            print("Error: Line number out of range.")
            return
        
        lines[line_number] = key_combo + '\n'
        
        with open('assets/state_data.txt', 'w') as file:
            file.writelines(lines)
