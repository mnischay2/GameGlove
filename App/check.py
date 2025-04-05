import combo
forward=["","",""]
backward=["","",""]
left=["","",""]
right=["","",""]
index=["","",""]
little=["","",""]
with open("assets/state_data.txt", "r") as file:
        data = file.read().split('\n')
        combo.seperate_key_combo(data[0], forward)
        combo.seperate_key_combo(data[1], backward)
        combo.seperate_key_combo(data[2], left)
        combo.seperate_key_combo(data[3], right)
        combo.seperate_key_combo(data[4], index)
        combo.seperate_key_combo(data[5], little)
        print("Forward 1: ", forward[0])
        print("Forward 2: ", forward[1])
        print("Forward 3: ", forward[2])
        print("Backward 1: ", backward[0])
        print("Backward 2: ", backward[1])
        print("Backward 3: ", backward[2])
        
