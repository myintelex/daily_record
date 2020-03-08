import random
import datetime

from faker import Faker

from daily_record import db
from daily_record.models import Habit, Record, Days, Category

fake = Faker()


def fake_data():
    db.create_all()
    Habit.query.delete()
    Record.query.delete()
    Days.query.delete()
    db.session.commit()

    count = 24
    categorys = ['Career', 'Finance', 'Social', 'Family', 'Health', 'Growth', 'Funny', 'Study']
    for cate in categorys:
        category = Category(name=cate)
        db.session.add(category)
        db.session.commit()
    
    for i in range(count):
        habit = Habit(
            name=fake.sentence(),
            category=categorys[random.randint(0, 7)],
            today_state=bool(random.getrandbits(1)),
            done_value=random.randrange(10, 100, 10),
            undone_value=random.randrange(10, 50, 10),
            total_done = 0,
            done_on_month = 0,
            continue_done = 0,
            max_continue_done = 0
        )
        db.session.add(habit)
        db.session.commit()
    
    habits = Habit.query.all()
    for i in range(0, 40):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=(40-i))
        fake_date = now - delta
        day_record = Days(
            date = fake_date
        )
        score = 0
        for hab in habits:                
            if fake_date.day == 1:
                hab.done_on_month = 0                
            record = Record(
                habit_id = hab.id,
                category = hab.category,
                state = random.getrandbits(1),
                date = fake_date
            )
            if bool(record.state):
                hab.total_done = int(hab.total_done) + 1
                hab.done_on_month = int(hab.done_on_month) + 1
                score = score + hab.done_value
                yester_date = fake_date - datetime.timedelta(days=1)
                ret = Record.query.filter_by(date = yester_date.date()).filter_by(habit_id = hab.id).all()
                if ret:
                    hab.continue_done = int(hab.continue_done) + 1
                else:
                    hab.continue_done = 1

                if hab.continue_done > hab.max_continue_done:
                    hab.max_continue_done = hab.continue_done
            else :
                if fake_date.day == 1:
                    hab.done_on_month = 0
                score = score - hab.undone_value
            db.session.add(record)
            db.session.commit()
            db.session.add(hab)
            db.session.commit()
            print("%s : add habit[%s] %s " %(now.date, hab.category, hab.name))

        day_record.score = score
        db.session.add(day_record)
        db.session.commit()
    
    
