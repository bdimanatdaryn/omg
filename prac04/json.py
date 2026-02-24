import json

data = '''
{
    "company": {
        "employees": [
            {"name": "Ali", "skills": ["Python", "SQL"]},
            {"name": "Dani", "skills": ["C++", "Java"]}
        ]
    }
}
'''

obj = json.loads(data)

print(obj["company"]["employees"][0]["skills"][1])

#2
import json

data = '{"name": "Ali", "age": 20}'
update = '{"age": 21, "city": "Almaty"}'

a = json.loads(data)
b = json.loads(update)

a.update(b)

print(json.dumps(a, indent=4))

#3
import json

data = '''
{
    "a": 5,
    "b": {
        "c": 10,
        "d": [1, 2, {"e": 7}]
    }
}
'''

obj = json.loads(data)

def find_numbers(x):
    if isinstance(x, dict):
        for value in x.values():
            find_numbers(value)
    elif isinstance(x, list):
        for item in x:
            find_numbers(item)
    elif isinstance(x, int) or isinstance(x, float):
        print("Found number:", x)

find_numbers(obj)
#4
import json

data = {"name": "Ali", "age": 20}

result = json.dumps(data)
print(result)