time1, time2 = input("input separated by a space: ").split(" ")
time1 = int(time1)
time2 = int(time2)
for i in range(1, 13):
    print(str(time1+(time2+i*5)//60)+':'+ f'{((time2+i*5)%60):02}')
    