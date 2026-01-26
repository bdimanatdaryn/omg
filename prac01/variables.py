#1 example
x= 5
y= "GGG"
print(x)
print (y)
#2 example
x=5
x="Hola"
print(x)
#3 example
x,y,z="Amanda","Linda","Rose"
print(x)
print(y)
print(z)
#4 example
lessons=["pp2","calculus","linear algebra"]
x,y,z=lessons
print (x)
print (y)
print (z)
#5 example
x="real"
def fff():
    global x
    x="fake"
fff()
print("it is "+x)