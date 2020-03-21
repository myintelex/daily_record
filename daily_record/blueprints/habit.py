import datetime

from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from daily_record.extensions import db
from daily_record.forms import DelHabitForm, AddHabitForm, EditHabitForm, DelHabitForm, LoginForm
from daily_record.models import Habit, Record, Category

habit_bp = Blueprint('habit', __name__)


@habit_bp.route('/new_habit', methods=['GET', 'POST'])
def new_habit():
    form = AddHabitForm()
    if form.validate_on_submit():
        habit = Habit(name=form.name.data,
                      category_name=form.category_name.data,
                      done_value=form.done_value.data,
                      undone_value=form.undone_value.data)
        db.session.add(habit)
        db.session.commit()
        return redirect(url_for('index.root'))
    return render_template('new_habit.html', form=form)


@habit_bp.route('/change_habit_state/<string:habit_id>', methods=['GET'])
def change_habit_state(habit_id):
    habit = Habit.query.get(habit_id)
    today_str = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
    args_date = request.args.get('date', today_str)
    date = datetime.datetime.strptime(args_date, '%Y-%m-%d').date()
    filters = {Record.date == date, Record.habit_id == habit_id}
    ret = Record.query.filter(*filters).one_or_none()
    state = True
    if ret:
        state = not ret.state
        db.session.delete(ret)
        db.session.commit()

    record = Record(habit_id=habit_id,
                    category_name=habit.category_name,
                    date=date,
                    state=state)
    if state:
        record.value = habit.done_value
    else:
        record.value = -habit.undone_value
    db.session.add(record)
    db.session.commit()
    habit.refresh_done_cnt()
    db.session.commit()

    return jsonify(habit_name=habit.name,
                   state=record.state,
                   habit_progress=habit.progress_this_month(),
                   total_cnt=habit.total_done,
                   continue_cnt=habit.continue_done,
                   category_name=habit.category_name,
                   category_cnt=habit.category.done_cnt()), 200


@habit_bp.route('/get_category_done_cnt/<string:category_name>',
                methods=['GET'])
def get_category_done_cnt(category_name):
    category = Category.query.filter_by(name=category_name).one()
    return jsonify(done_cnt=category.done_cnt(),
                   total_cnt=len(category.habits))


@habit_bp.route('/edit_habit/<int:habit_id>', methods=['GET', 'POST'])
def edit_habit(habit_id):
    form = EditHabitForm()
    habit = Habit.query.get(habit_id)
    if form.validate_on_submit():
        habit.name = form.name.data
        habit.category_name = form.category_name.data
        habit.done_value = form.done_value.data
        habit.undone_value = form.undone_value.data
        db.session.commit()
        return redirect(url_for('index.root'))        
    form.name.data = habit.name
    form.category_name.data = habit.category_name
    form.done_value.data = habit.done_value
    form.undone_value.data = habit.undone_value
    return render_template('edit_habit.html', form=form, id=habit_id)

@habit_bp.route('/del_habit/<int:habit_id>', methods=['POST', 'GET'])
def del_habit(habit_id):
    habit = Habit.query.get(habit_id) 
    form = DelHabitForm()
    if form.validate_on_submit():
        db.session.delete(habit)
        db.session.commit()
        return redirect(url_for('index.root'))        
    return render_template('habit_del.html',form=form, id=habit_id, habit_name=habit.name)

