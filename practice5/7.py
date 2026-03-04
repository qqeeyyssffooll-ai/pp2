import re
s = input()
def convert(match):
    return match.group(1).upper()
txt = re.sub("_([a-z])", convert, s)
print(txt)