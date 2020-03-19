import random
import datetime

from faker import Faker

from daily_record.extensions import db
from daily_record.models import Habit, Record, Category

fake = Faker()


def fake_data():
    db.create_all()
    Habit.query.delete()
    Record.query.delete()
    db.session.commit()

    count = 24
    categorys = [
        'Career', 'Finance', 'Social', 'Family', 'Health', 'Growth', 'Funny',
        'Study'
    ]
    for cate in categorys:
        category = Category(name=cate)
        db.session.add(category)
        db.session.commit()
        for i in range(random.randint(3, 7)):
            habit = Habit(name=fake.sentence(),
                          category_name=cate,
                          today_state= False,
                          done_value=random.randrange(10, 100, 10),
                          undone_value=random.randrange(0, 50, 10),
                          total_done=0,
                          done_on_month=0,
                          continue_done=0,
                          max_continue_done=0)
            db.session.add(habit)
            db.session.commit()

    habits = Habit.query.all()
    for i in range(0, 300):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=(300 - i))
        fake_date = now - delta
        score = 0
        for hab in habits:
            record = Record(habit_id=hab.id,
                            category_name=hab.category_name,
                            state=random.getrandbits(1),
                            date=fake_date)
            if record.state:
                record.value = hab.done_value
            else:
                record.value = -hab.undone_value

            db.session.add(record)
        print("%s : add over " % (fake_date.strftime('%Y-%m-%d') ))
    db.session.commit()

