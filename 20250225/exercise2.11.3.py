import math

#part1

r = int(input("半徑="))
radius = 4/3*math.pi*r*r*r
print ("面積為=",radius)

#part2

x = int(input("輸入一個整數="))
c = math.pow(math.cos(x),2)+math.pow(math.sin(x),2)
print ("輸出為:",c)


