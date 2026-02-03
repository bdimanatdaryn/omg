#1 example
s="Awesome"
print(s[3:])
#2 example
s=str("very1234")
for x in range(len(s)):
    print(s[x],end=" ")
#3 example
text="She is so cool"
if "cool" in text:
    print("True")

else:
    print("False")
#4 exmaple
a="Arsenal is the best club in the London"
print(a.replace("Arsenal","Chelsea"))
#5 example
name="Tima"
age=35
text=f"My name is {name},I am {age} years old"
print(text)