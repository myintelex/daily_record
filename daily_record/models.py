from flask import jsonify
import datetime
import calendar

from daily_record.extensions import db


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category_name = db.Column(db.Text, db.ForeignKey('category.name'))
    category = db.relationship('Category', back_populates='habits')
    records = db.relationship('Record')
    done_value = db.Column(db.Integer)
    undone_value = db.Column(db.Integer)

    today_state = db.Column(db.Boolean, default=False)
    total_done = db.Column(db.Integer, default=0)
    done_on_month = db.Column(db.Integer, default=0)
    continue_done = db.Column(db.Integer, default=0)
    max_continue_done = db.Column(db.Integer, default=0)

    def progress_this_month(self):
        today = datetime.datetime.today()
        monthRange = calendar.monthrange(today.year, today.month)[1]
        ret = {
            'progress': self.done_on_month * 100 / today.day,
            'state': 'bg-danger'
        }
        if ret['progress'] > 80:
            ret['state'] = 'bg-success'
        elif ret['progress'] > 60:
            ret['state'] = 'bg-primary'
        return ret

    def prev_7_records(self):
        today = datetime.date.today()
        sign_list = ['-', 'M', 'T', 'W', 'T', 'F', 'S', 'S']

        # sign_list = ['-','一','二','三','四', '五','六','日']
        # record = Record.query.filter(Record.date==today).filter(Record.habit_id==self.id).first_or_404()
        def _get_day_state(x):
            # state = {'state': False, 'days': sign_list[(today -datetime.timedelta(days=x)).isoweekday()]}
            d = (today - datetime.timedelta(days=x))
            state = {'state': False, 'days': d.day, 'date': d}
            ret = list(
                filter(lambda r: r.date == today - datetime.timedelta(days=x),
                       self.records))
            if ret and ret[0].state:
                state['state'] = True
            return state

        re = list(map(_get_day_state, [6, 5, 4, 3, 2, 1, 0]))
        return re

    def add_undone_record(self):
        def _add_undone_record(habit, day):
            records = Record.query.filter_by(date=day).filter_by(
                habit_id=habit.id).all()
            if records:
                return
            record = Record(habit_id=habit.id,
                            category=habit.category,
                            state=False,
                            date=day,
                            value=-habit.undone_value)
            db.session.add(record)
            db.session.commit()
            oneday = datetime.timedelta(days=1)
            prev_day = day - oneday
            return _add_undone_record(habit, prev_day)

        return _add_undone_record(self, datetime.date.today())

    def refresh_done_cnt(self):
        self.today_state = Record.query.filter_by(
            date=datetime.date.today()).filter_by(
                habit_id=self.id).first().state
        done_records = list(filter(lambda record: record.state, self.records))
        self.total_done = len(done_records)
        done_records_this_month = list(
            filter(lambda r: r.date.month == datetime.date.today().month,
                   done_records))
        self.done_on_month = len(done_records_this_month)
        self.continue_done = self._recent_continue_days()
        self.max_continue_done = self._max_continue_days()

    def _recent_continue_days(self):
        records = sorted(self.records,
                         key=lambda record: record.date,
                         reverse=True)
        i = 0
        while (i < len(records) and records[i].state):
            i = i + 1
        return i

    def _max_continue_days(self):
        records = sorted(self.records,
                         key=lambda record: record.date,
                         reverse=True)
        len = 0
        tmp = 0
        for record in records:
            if record.state:
                tmp = tmp + 1
                if tmp > len:
                    len = tmp
            else:
                tmp = 0
        return len


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'))
    habit = db.relationship('Habit', back_populates='records')
    category_name = db.Column(db.Integer, db.ForeignKey('category.name'))
    category = db.relationship('Category', back_populates='records')

    state = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date, default=datetime.date.today())
    value = db.Column(db.Integer)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    records = db.relationship('Record')
    habits = db.relationship('Habit')

    def done_cnt(self):
        return len(list(filter(lambda habit: habit.today_state, self.habits)))


@db.event.listens_for(Habit, 'after_insert', named=True)
def insert_habit(**kwargs):
    habit = kwargs['target']
    record = Record(habit_id=habit.id,
                    category_name=habit.category_name,
                    value=-habit.undone_value)
    db.session.add(record)
