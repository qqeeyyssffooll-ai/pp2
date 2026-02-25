def fun(max):
    cnt = 0
    while cnt <= max:
        yield cnt 
        cnt += 2

a = int(input())

first = True
for n in fun(a):
    if not first:
        print(",", end="")
    print(n, end="")
    first = False