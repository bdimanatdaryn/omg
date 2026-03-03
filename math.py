#1
import math

degree = float(input())

radian = degree * math.pi / 180

print(radian)
#2
import math
Height=int(input())
Basef=int(input())
Bases=int(input())
print((Basef+Bases)/2*Height)

#3 
import math

n = int(input())
a = float(input())

area = (n * a * a) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", area)
#4
base = float(input())
height = float(input())

area = base * height

print(area)