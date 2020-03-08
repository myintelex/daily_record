
import datetime


today = datetime.date.today()
week_start_day = today - datetime.timedelta(days=today.weekday())
for day in range(0, today.weekday()):
    print(day)

print(today.weekday())


class ClassA:
    def __init__(self, date, value): 
        self.date = date 
        self.value = value

    def show(self): 
        print("Class:date %s, value%d" % (str(self.date.__str__()), int(self.value)))


test_list = [ClassA(datetime.date(2018, 9, 12), 13), ClassA(datetime.date(2018, 9, 19), 13), ClassA(
    datetime.date(2018, 7, 12), 13), ClassA(datetime.date(2028, 9, 12), 23), ClassA(datetime.date(2014, 9, 12), 17) ]

print('order1-------------------------')
order1 = list(sorted(test_list, key=lambda x: x.date))
for o in order1:
    o.show()

def date_detal(x, y):
    