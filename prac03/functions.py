#1 ex
def my(dname):
    print(dname+" cool")
n=input()
my(n)
#2 ex
def check_even(n):
    if n % 2 == 0:
        return "Even"
    else:
        return "Odd"

print(check_even(4))
print(check_even(7))
#3 ex 
def changecase(func):
  def myinner():
    return func().upper()
  return myinner

@changecase
def my():
  return "hey Daryn"

@changecase
def other():
  return "only lowers here"

print(my())
print(other())
#4 ex 
def factorial(n):
   if n == 1 or n == 0:
      return 1
   
   return n*factorial(n-1)
n=int(input())
factorial(n)