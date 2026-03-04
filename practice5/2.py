import re
s = input()
txt = re.match(r"ab{2,3}", s)
print(txt)