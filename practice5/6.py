import re
s = input()
txt = re.sub("[ ,.]+", ":", s)
print(txt)