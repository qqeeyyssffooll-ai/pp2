import re
s = input()
txt = re.findall("^a.*b$", s)
print(txt)