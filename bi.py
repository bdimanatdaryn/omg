from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# 1
mapped = list(map(lambda x: x * 2, numbers))
print("map result:", mapped)

# 2
filtered = list(filter(lambda x: x % 2 == 0, numbers))
print("filter result:", filtered)

# 3
reduced = reduce(lambda a, b: a + b, numbers)
print("reduce result:", reduced)

# 4
names = ["Ali", "Dana", "Ramazan"]

for index, name in enumerate(names):
    print(index, name)

# 5
ages = [20, 21, 22]

for name, age in zip(names, ages):
    print(name, age)

# 6
x = "25"

print("Type of x:", type(x))

x_int = int(x)
print("Converted to int:", x_int)

print("Type after conversion:", type(x_int))