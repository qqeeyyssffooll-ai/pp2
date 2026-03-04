import re
s = input()
def convert(match):
    return "_" + match.group(1).lower()
txt = re.sub("([A-Z])", convert, s)
print(txt)