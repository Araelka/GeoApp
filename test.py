import random
ls = {}
for i in range(0,50):
    ls[i] = random.randrange(-10,10)
for i in range(50, 101):
    ls[i] = random.randrange(0,11)
max = 0
min = 0
for i in ls:
    if ls[i] < 0:
        min += ls[i]
    else:
        max += ls[i]
    if abs(max) > abs(min):
        print(i)
        print(ls)
        break
print(f"min: {min}\nmax: {max}")
