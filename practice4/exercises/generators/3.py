def gen(par):
    cnt = 0
    while cnt < par:
        yield cnt
        cnt += 12

n = int(input())
for i in gen(n):
    print(i, end=" ")