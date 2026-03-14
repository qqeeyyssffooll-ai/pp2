import os

path = "class"

for root, dirs, files in os.walk(path):
    print("Directory:", root)
    
    for d in dirs:
        print(" Dir:", d)
    
    for f in files:
        print(" File:", f)

