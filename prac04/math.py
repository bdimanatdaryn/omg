#1
import math

a = 2
b = 5
c = -3

D = b*b - 4*a*c

if D >= 0:
    x1 = (-b + math.sqrt(D)) / (2*a)
    x2 = (-b - math.sqrt(D)) / (2*a)
    print(x1, x2)
else:
    print("No real roots")

#2
import math

x1, y1 = 1, 2
x2, y2 = 6, 8

d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
print(d)

#3
import math

x = 3
print(math.exp(x))

#4
import math

print(math.log(100))   
print(math.log10(100))    
print(math.log(8, 2))    