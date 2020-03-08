from flask import jsonify
from daily_record import db, ma
import datetime

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text, db.ForeignKey('category.name'))
    today_state = db.Column(db.Boolean)
    done_value = db.Column(db.Integer)
    undone_value = db.Column(db.Integer)
    total_done = db.Column(db.Integer)
    done_on_month = db.Column(db.Integer)
    continue_done = db.Column(db.Integer)
    max_continue_done = db.Column(db.Integer)
    records = db.relationship('Record')

    def refresh_done_cnt(self):
        done_records=list(filter(lambda record: record.state, self.records))
        self.total_done = len(done_records)
        done_records_this_month = list(filter(lambda r: r.date.month == datetime.date.today().month, done_records))
        self.done_on_month = len(done_records_this_month)
        self.continue_done = self._recent_continue_days()
        self.max_continue_done = self._max_continue_days()
        print(self.name + "----------------------------------------")
        print(self.total_done)


    def _recent_continue_days(self):
        records = sorted(self.records, key=lambda record: record.date, reverse=True)
        i = 0
        while(i < len(records) and records[i].state):
            i = i+1
        return i

    def _max_continue_days(self):
        records = sorted( self.records, key=lambda record: record.date, reverse=True)
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
    category = db.Column(db.Integer, db.ForeignKey('category.name'))
    state = db.Column(db.Boolean)
    date = db.Column(db.Date)

class Days(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    date = db.Column(db.Date)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    records = db.relationship('Record')
    habits = db.relationship('Habit')

class RecordSchema(ma.ModelSchema):
    class Meta:
        model=Record

class HabitSchema(ma.ModelSchema):
    class Meta:
        model=Habit

class CategorySchema(ma.ModelSchema):
    class Meta:
        model=Category
    
    habits = ma.Nested(HabitSchema, many=True)
    records = ma.Nested(RecordSchema, many=True)

