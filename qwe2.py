count = int(input("count people:"))
y, n = 0, 0
for i in range(count):
    if int(input("1 or 2 or 3")) == 2:
        n += 1
    else:
        y += 1
print(int(y/(y+n) * 100))
