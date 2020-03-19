from flask import Flask, render_template, url_for, flash, redirect, json, jsonify, abort, request
from functools import reduce
from sqlalchemy.sql import func

from daily_record import app, db
from daily_record.forms import DelHabitForm, AddHabitForm, EditHabitForm, DelHabitForm, LoginForm
from daily_record.models import Habit, Record, Category
from daily_record.fake import fake_data

import datetime


@app.template_filter()
def done_cnt(habits):
    return list(filter(lambda habit: habit.today_state, habits))


@app.template_filter()
def prev_7_record(habits):
    today = datetime.date.today()
    sign_list = ['-','M','T','W','T','F','S','S']
    def get_day_state(x):
        state = {'state': False, 'days': sign_list[(today -datetime.timedelta(days=x)).isoweekday()]}
        ret = list(filter(lambda r: r.date == today -datetime.timedelta(days=x), habits.records))
        if ret and ret[0].state:
            state['state'] = True
        return state

    re = list(map(get_day_state, range(0,7)))
    prev_7_date = datetime.date.today() - datetime.timedelta(days=7)
    return re


@app.route('/', methods=['POST', 'GET'])
def root():
    habits = Habit.query.all()
    for habit in habits:
        habit.
    return render_template('base.html')


@app.route('/get_total_score', methods=['GET'])
def get_total_score():
    score = Record.query.with_entities(func.sum(Record.value)).all()
    return jsonify(score)


@app.route('/get_month_score', methods=['GET'])
def get_month_score():
    today = datetime.date.today()
    filters = {
        Record.date > datetime.date(today.year, today.month, 1) - datetime.timedelta(1)
    }
    score = Record.query.filter(*filters).with_entities(func.sum(
        Record.value)).all()
    return jsonify(score)

@app.route('/get_prev_month_score', methods=['GET'])
def get_prev_month_score():
    today = datetime.date.today()
    prev_m_last_day = datetime.date(today.year, today.month, 1) - datetime.timedelta(1)
    filters = {
        Record.date <= prev_m_last_day,
        Record.date >= datetime.date(prev_m_last_day.year, prev_m_last_day.month, 1)
    }
    score = Record.query.filter(*filters).with_entities(func.sum(
        Record.value)).all()
    return jsonify(score)

@app.route('/photos', methods=['POST', 'GET'])
def photos():
    return render_template('photos.html')


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    return render_template('blog.html')


@app.route('/show_habit_list', methods=['GET'])
def show_habit_list():
    categorys = Category.query.all()
    return render_template('habit_list.html',
                           categorys=categorys,
                           datetime=datetime)


@app.route('/habit_list', methods=['GET'])
def habit_list():
    habits = Habit.query.all()
    for habit in habits:
        today = datetime.date.today()
        add_undone_record(habit, today)
        habit.today_state = Record.query.filter_by(
            date=datetime.date.today()).filter_by(
                habit_id=habit.id).first().state
        habit.refresh_done_cnt()
        db.session.commit()
    categorys = Category.query.all()
    records = Record.query.all()
    list1 = [10 for i in records if i.state]
    record = reduce(lambda x, y: x + y, list1)
    return jsonify(html=render_template('habit_list.html',
                                        categorys=categorys,
                                        datetime=datetime),
                   record=record)


@app.route('/setting', methods=['GET'])
def setting():
    return jsonify(html=render_template('setting.html'))


def add_undone_record(habit, day):
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
    return add_undone_record(habit, prev_day)


@app.route('/charts', methods=['POST', 'GET'])
def charts():
    categorys = Category.query.all()
    return jsonify(html=render_template('charts.html'),
                   categorys=list(map(lambda c: c.name, categorys)))


@app.route('/get_history_data/', methods=['GET'])
def get_history_data():
    type = request.args.get('type', 'Value')
    record_data = {}
    categorys = Category.query.all()
    category_names = list(map(lambda cate: cate.name, categorys))

    def _reduce_records_date(prev_record, next_record):
        if not next_record.date.strftime('%Y-%m-%d') in record_data:
            record_data[next_record.date.strftime('%Y-%m-%d')] = {
                'date': next_record.date.strftime('%Y-%m-%d')
            }
            for name in category_names:
                record_data[next_record.date.strftime('%Y-%m-%d')][name] = 0
        return record_data

    record_data = {}

    def _fun_cal_cnt(record):
        if record.state:
            date = record.date.strftime("%Y-%m-%d")
            record_data[date][
                record.category] = record_data[date][record.category] + 1

    def _fun_cal_value(record):
        date = record.date.strftime("%Y-%m-%d")
        record_data[date][record.category] = record_data[date][
            record.category] + int(record.value)

    records = Record.query.all()
    records = reduce(_reduce_records_date, records)
    for category in categorys:
        for record in category.records:
            if type == 'value':
                _fun_cal_value(record)
            else:
                _fun_cal_cnt(record)

    records = list(record_data.values())

    def _fun_cal_total(record):
        total = 0
        for c in record:
            if c != "date":
                total = total + record[c]
        record['value'] = total
        return record

    records = list(map(_fun_cal_total, records))
    return jsonify(records)


@app.route('/get_category_data', methods=['GET'])
def get_category_data():
    categorys = Category.query.all()
    result = []
    for category in categorys:
        category_data = {'name': category.name, 'value': 0, 'habits': []}
        for habit in category.habits:
            habit_data = {'name': habit.name, 'value': 0}
            for record in habit.records:
                if record.state:
                    habit_data['value'] = habit_data['value'] + 1
            category_data['habits'].append(habit_data)
            category_data[
                'value'] = category_data['value'] + habit_data['value']
        result.append(category_data)
    return jsonify(result)


@app.route('/new_habit', methods=['GET', 'POST'])
def new_habit():
    form = AddHabitForm()
    if form.validate_on_submit():
        name = form.name.data
        category = form.category.data
        habit = Habit(name=form.name.data,
                      category=form.category.data,
                      done_value=form.done_value.data,
                      undone_value=form.undone_value.data,
                      total_done=0,
                      done_on_month=0,
                      continue_done=0,
                      max_continue_done=0)
        db.session.add(habit)
        db.session.commit()
        record = Record(habit_id=habit.id,
                        category=habit.category,
                        state=False,
                        date=datetime.date.today())
        db.session.add(record)
        db.session.commit()
        flash('New Habit Added!')
        return redirect(url_for('root'))
    return render_template('new_habit.html', form=form)


@app.route('/edit_habit/<int:habit_id>', methods=['GET'])
def edit_habit(habit_id):
    form = EditHabitForm()
    habit = Habit.query.get(habit_id)
    form.name.data = habit.name
    form.category.data = habit.category
    form.done_value.data = habit.done_value
    form.undone_value.data = habit.undone_value
    return render_template('edit_habit.html', form=form, id=habit_id)


@app.route('/edit_habit/<int:habit_id>', methods=['POST'])
def post_edit_habit(habit_id):
    form = EditHabitForm()
    habit = Habit.query.get(habit_id)
    if form.validate_on_submit():
        habit.name = form.name.data
        habit.category = form.category.data
        habit.done_value = form.done_value.data
        habit.undone_value = form.undone_value.data
        db.session.commit()
        return redirect(url_for('root'))


@app.route('/del_habit/<int:habit_id>', methods=['POST'])
def del_habit(habit_id):
    habit = Habit.query.get(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return jsonify(message='Delete the data success.')


@app.route('/change_habit_state/<int:habit_id>', methods=['POST'])
def change_habit_state(habit_id):
    habit = Habit.query.get(habit_id)
    habit.today_state = not habit.today_state
    db.session.commit()

    ret = Record.query.filter_by(date=datetime.date.today()).filter_by(
        habit_id=habit_id).all()
    if ret:
        for record in ret:
            db.session.delete(record)
            db.session.commit()

    record = Record(habit_id=habit_id,
                    category=habit.category,
                    date=datetime.date.today(),
                    state=habit.today_state)
    if habit.today_state:
        record.value = habit.done_value
    else:
        record.value = -habit.undone_value
    db.session.add(record)
    db.session.commit()
    habit.refresh_done_cnt()
    db.session.commit()

    return jsonify(state=habit.today_state), 200
