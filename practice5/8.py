import re
s = input()
txt = re.split("(?=[A-Z])", s)
print(txt)