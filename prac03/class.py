#1 ex
class MyClass:
  x = 5

p3 = MyClass()
print(p3.x)
#2 ex
class DA:
  def __init__(self,name,age):
    self.name=name
    self.age=age
p1=DA("DARYN",18)
print(p1.name)
print(p1.age)
#3 ex
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def hi(self):
    print("He is " + self.name)
    print("his age is" , self.age)

p1 = Person("Daryn", 18)
p1.hi()
#4 ex
class da:
  prof="Nurse"
  def __init__(self, name):
    self.name = name

p1 = da("Daryn")
p2 = da("Adai")

print(p1.name)
print(p2.name)
print(p1.prof)
print(p2.prof)