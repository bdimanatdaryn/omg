from datetime import datetime

def years_between(start, end):
    year = start.year
    while year <= end.year:
        yield year
        year += 1

for y in years_between(datetime(2020,1,1), datetime(2025,1,1)):
    print(y)

#2
from datetime import datetime

def months_of_year(year):
    for m in range(1, 13):
        yield datetime(year, m, 1)

for d in months_of_year(2024):
    print(d.strftime("%Y-%m-%d"))

#3
from datetime import datetime

def days_in_month(year, month):
    day = 1
    while True:
        try:
            yield datetime(year, month, day)
            day += 1
        except ValueError:
            break

for d in days_in_month(2024, 2):
    print(d.strftime("%Y-%m-%d"))

#4 
def leap_years(start, end):
    for year in range(start, end + 1):
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            yield year

for y in leap_years(2000, 2030):
    print(y)