#1
def squares(n):
    for i in range(n):
        yield i * i

for x in squares(5):
    print(x)

#2
def infinite_counter():
    i = 1
    while True:
        yield i
        i += 1

gen = infinite_counter()

for _ in range(5):
    print(next(gen))

#3
def words(text):
    for word in text.split():
        yield word

for w in words("Hello Ramazan my brother"):
    print(w)

#4
def powers_of_two(n):
    value = 1
    for _ in range(n):
        yield value
        value *= 2

for x in powers_of_two(6):
    print(x)

#5
def prime_generator(numbers):
    for num in numbers:
        if num < 2:
            continue
        
        is_prime = True
        
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        
        if is_prime:
            yield num


nums = [1, 2, 3, 4, 5, 6, 17, 20, 23, 24]

for p in prime_generator(nums):
    print(p)