import re
s = input()
txt = re.findall("[a-z]+(?:_[a-z]+)+", s)
print(txt)