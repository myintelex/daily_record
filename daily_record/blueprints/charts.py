import datetime

from sqlalchemy.sql import func
from functools import reduce
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from daily_record.extensions import db
from daily_record.models import Habit, Record, Category

charts_bp = Blueprint('charts', __name__)


@charts_bp.route('/get_history_data/', methods=['GET'])
def get_history_data():
    type = request.args.get('type', 'Value')

    if type == 'Value': 
        date_query = db.session.query(Record.date, func.sum(Record.value))
    else:
        date_query = db.session.query(Record.date, func.count()).filter_by(state=True)
    date_value = date_query.group_by(Record.date).all()

    ret = []
    for d in date_value:
        date, value = d
        item = {'date': date.strftime('%Y-%m-%d'), 'value': value}
        if type == 'Value': 
            cate_query = db.session.query(Record.category_name, func.sum(Record.value))
        else:
            cate_query = db.session.query(Record.category_name, func.count()).filter_by(state=True)
        cate_values = cate_query.filter_by(date=date).group_by(Record.category_name).all()
        for cate_value in cate_values:
            name, value = cate_value
            item[name] = value
        ret.append(item)
    categorys = db.session.query(Category.name).all()
    return jsonify(data=ret, categorys=categorys)


@charts_bp.route('/get_category_data', methods=['GET'])
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
