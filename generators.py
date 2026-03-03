#1
def sqr(n):
    for i in range(n):
        yield i**2

n=int(input())
print(*sqr(n),sep=",")

#2 
def s(n):
    for i in range(0,n+1):
        if i%2==0:
            yield i

n=int(input())
print(*s(n),sep=",")

#3
def da(n):
    for i in range(0,n+1):
        if i%3==0 and i%4==0:
            yield i

n=int(input())
print(*da(n),sep=",")

#4 
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

for value in squares(2, 6):
    print(value)

#5
def count(n):
    for i in range(n, -1, -1):
        yield i

for num in count(5):
    print(num)