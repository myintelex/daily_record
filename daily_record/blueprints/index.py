import datetime

from flask import Flask, Blueprint, render_template, jsonify
from sqlalchemy import func

from daily_record.models import Category, Habit, Record

index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET'])
@index_bp.route('/index', methods=['GET'])
def root():
    habits = Habit.query.all()
    for habit in habits:
        habit.add_undone_record()
        habit.refresh_done_cnt()
    return render_template('base.html')


@index_bp.route('/get_total_score', methods=['GET'])
def get_total_score():
    score = Record.query.with_entities(func.sum(Record.value)).all()
    return jsonify(score[0][0])


@index_bp.route('/get_month_score', methods=['GET'])
def get_month_score():
    today = datetime.date.today()
    filters = {
        Record.date >
        datetime.date(today.year, today.month, 1) - datetime.timedelta(1)
    }
    score = Record.query.filter(*filters).with_entities(func.sum(
        Record.value)).all()
    return jsonify(score[0][0])


@index_bp.route('/get_prev_month_score', methods=['GET'])
def get_prev_month_score():
    today = datetime.date.today()
    prev_m_last_day = datetime.date(today.year, today.month,
                                    1) - datetime.timedelta(1)
    filters = {
        Record.date <= prev_m_last_day, Record.date >= datetime.date(
            prev_m_last_day.year, prev_m_last_day.month, 1)
    }
    score = Record.query.filter(*filters).with_entities(func.sum(
        Record.value)).all()
    score = score[0][0]
    if not score:
        score = 0
    return jsonify(score)


@index_bp.route('/show_habit_list', methods=['GET'])
def show_habit_list():
    categorys = Category.query.all()
    return render_template('habit_list.html',
                           categorys=categorys,
                           datetime=datetime)


@index_bp.route('/show_habit_charts', methods=['GET'])
def show_habit_charts():
    return render_template('habit_charts.html')


@index_bp.route('/get_categorys_name', methods=['GET'])
def get_categorys_name():
    categorys = Category.query.all()
    return jsonify([x.name for x in categorys])

@index_bp.route('/get_done_on_total_today', methods=['GET'])
def get_done_on_total_today():
    return jsonify(done=Habit.query.filter_by(today_state=True).count(), total=Habit.query.count())