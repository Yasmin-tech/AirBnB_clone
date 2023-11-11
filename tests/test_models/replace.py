#!/usr/bin/python3

with open("./test_amenity.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_list = []
for line in lines:
        if "s4" in line:
                new_line = line.replace("s4", "a4")
                new_list.append(new_line)
        else:
                new_list.append(line)
with open("./test_amenity.py", "w", encoding="utf-8") as f:
       f.writelines(new_list)