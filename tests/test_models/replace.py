#!/usr/bin/python3

with open("./test_user.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_list = []
for line in lines:
        if "BaseModel" in line:
                new_line = line.replace("BaseModel", "User")
                new_list.append(new_line)
        else:
                new_list.append(line)
with open("./test_user.py", "w", encoding="utf-8") as f:
       f.writelines(new_list)