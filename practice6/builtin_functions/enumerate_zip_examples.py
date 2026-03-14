words = ["a", "b", "c"]
nums = [1, 2, 3]

for i, x in enumerate(words):
    print(i, x)

for x, y in zip(words, nums):
    print(x, y)