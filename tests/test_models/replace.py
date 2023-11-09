#!/usr/bin/python3

with open("./test_user.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("./test_user.py", "w", encoding="utf-8") as f:
    for line in lines:
        if "b1" in line:
            line.replace("b1", "u1")
        f.write(line)
