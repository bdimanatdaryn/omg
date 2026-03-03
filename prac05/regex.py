#1

import re

s = input()
pattern = r"ab*"

print(bool(re.fullmatch(pattern, s)))

#2
import re

s = input()
pattern = r"ab{2,3}"

print(bool(re.fullmatch(pattern, s)))

#3
import re

s = input()
pattern = r"[a-z]+_[a-z]+"

print(re.findall(pattern, s))

#4
import re

s = input()
pattern = r"[A-Z][a-z]+"

print(re.findall(pattern, s))
#5
import re

s = input()
pattern = r"a.*b"

print(bool(re.fullmatch(pattern, s)))
#6
import re

s = input()
result = re.sub(r"[ ,\.]", ":", s)

print(result)
#7
s = input().strip()

parts = s.split("_")
camel = parts[0] + "".join(word.capitalize() for word in parts[1:])

print(camel)
#8
import re

s = input().strip()
parts = re.findall(r"[A-Z][a-z]*", s)

print(parts)          # список
print(" ".join(parts))  # строка
#9
import re

s = input().strip()
result = re.sub(r"(?<!^)([A-Z])", r" \1", s)

print(result)
#10
import re

s = input().strip()
result = re.sub(r"(?<!^)([A-Z])", r"_\1", s).lower()

print(result)