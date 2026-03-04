import re
s = input()
txt = re.sub("([A-Z])", r" \1", s)
print(txt)