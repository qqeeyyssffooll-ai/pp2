import math
numbers = int(input("Input number of sides: "))
length = int(input("Input the length of a side: "))
area = (numbers*(length**2))/(4*math.tan(math.pi/numbers))
print("The area of the polygon is:", math.floor(area))