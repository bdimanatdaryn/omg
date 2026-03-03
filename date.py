from datetime import datetime, timedelta

today = datetime.today().date()
new_date = today - timedelta(days=5)

print(new_date)

#2
from datetime import datetime, timedelta

today = datetime.today().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:",today)
print("Tomorrow:",tomorrow)
#3
from datetime import datetime

now = datetime.now()

print(now.strftime("%Y-%m-%d %H:%M:%S"))

#4 
from datetime import datetime,timedelta

date1=datetime(2026,5,23,15,30,0)
date2=datetime(2026,5,20,14,5,23)

difference = date1 - date2

s=difference.total_seconds()
print(int(s))