#1 example
n=int(input())
while n:
    print(n)
    n-=1
#2 example
n=20
while n>10:
    if n<19:
        break
    print(n)
    n-=1
#3 example
i=0
while i<10:
    i+=1
    if i==3:
        continue
    print(i)
#4 example
a="Hello"
for i in a:
    print (i)
#5 example
a="Hello"
for i in a:
    if i=="l":
        break
    print(i)
#6 example
a=25
for i in range(a):
    if i>=20:
        continue
    print(i)