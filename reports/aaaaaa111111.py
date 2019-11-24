import random
from datetime import date, datetime

dates = []
for i in range(20): # generate 20 random dates
    mo = random.randint(1, 12)
    day = random.randint(1, 28)
    yr = random.randint(2014, 2019)
    dates.append(date(yr, mo, day))

# for d in dates:
#     print(d)

new_dates = [random.choice(dates) for i in range(20)]

for nd in new_dates:
    print (nd)



# mo = random.randint(1, 12)
# day = random.randint(1, 28)
# yr = random.randint(2014, 2019)
# dates = [date(yr, mo, day) for i in range(20)]
#

