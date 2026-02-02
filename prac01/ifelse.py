#1 example
a=47
if 47%2!=0:
    print("odd number")
#2 example
a=int(input())
if a%2==0:
    print("even")
elif a%2!=0:
    print("Odd")
#3 example
a=879
b=897
if a>b:
    print("a is greater than b")
else:
    print("b is greater than a")
#4 example
a=5
b=6
if b>a: print("b greater")
#5 example
age=int(input())
have_pasport=True
if age>=18:
    if have_pasport:
        print("You can come in")
    else:
        print("YOu can not come in")
elif age<18:
    print("you can not come in")