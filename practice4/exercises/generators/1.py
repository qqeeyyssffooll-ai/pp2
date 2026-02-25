def gen(par):
    cnt = 1
    while cnt <= par:
        yield cnt**2
        cnt += 1

N = int(input())
for i in gen(N):
    print(i, end=" ")