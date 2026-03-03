import re
import json

with open("raw.txt", "r",encoding="utf-8") as f:
    text = f.read()

prices = re.findall(r"\d+\.\d{2}|\d+,\d{2}", text)

prices = [float(p.replace(",", ".")) for p in prices]

#2

date = re.search(r"\d{2}[./-]\d{2}[./-]\d{2,4}", text)
time = re.search(r"\d{2}:\d{2}", text)

date = date.group() if date else None
time = time.group() if time else None


# 3

payment_method = None

if re.search(r"cash|налич", text, re.IGNORECASE):
    payment_method = "Cash"
elif re.search(r"card|visa|mastercard|карт", text, re.IGNORECASE):
    payment_method = "Card"


# 4

lines = text.split("\n")
products = []

for i in range(len(lines)):
    line = lines[i]

    # ищем строки типа "2,000 x 154,00"
    if re.search(r"x", line) and re.search(r"\d+[.,]\d{2}", line):
        if i > 0:
            name = lines[i - 1].strip()
            products.append(name)

# 5

total = sum(prices)

#6 

result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "prices": prices,
    "products": products,
    "total_calculated": round(total, 2)
}

print(json.dumps(result, indent=2, ensure_ascii=False))