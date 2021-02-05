import csv
import datetime
import random
import string

with open(f'media/csv_file|{datetime.datetime.now().timestamp()}.csv', 'w', newline='') as csv_file:
    f_csv = csv.writer(csv_file, delimiter='|',  doublequote='`', quoting=csv.QUOTE_MINIMAL)
    for i in range(int(5)):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        integ = str(random.randrange(10))
        f_csv.writerow([name, integ])