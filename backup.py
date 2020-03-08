import os
import uuid
import sys
from flask import Flask, render_template, redirect, url_for, flash, session, send_from_directory, abort
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.csrf import validate_csrf
from flask_sqlalchemy import SQLAlchemy

import click

from forms import LoginForm, RecordForm, uploadForm, addHabitForm, editHabitForm, delHabitForm

app = Flask(__name__)
app.config.from_pyfile('setting.py')



db = SQLAlchemy(app)
@app.cli.command()
def hello():
    click.echo('hello world')

@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized Habit database success')
    
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    record = db.relationship('Record')

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Boolean)
    state = db.Column(db.Date)

@app.route('/newHabit', methods=['GET', 'POST'])
def new_note():
    form = addHabitForm()
    if form.validate_on_submit():
        name = form.name.data
        habit = Habit(name=name)
        db.session.add(habit)
        db.session.commit()
        flash('New Habit Added!')
        return redirect(url_for('index'))
    return render_template('newHabit.html', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome %s' % username)
        return redirect(url_for('index'))

    return render_template('basic.html', form=form)


@app.route('/')
@app.route('/index')
def index():
    form=delHabitForm()
    habits = Habit.query.all()
    return render_template('index.html', habits=habits, form=form)




def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    uploadform = uploadForm()
    if uploadform.validate_on_submit():
        f = uploadform.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success.')
        session['filenames'] = [filename]
        return redirect(url_for('index'))
    return render_template('upload.html', uploadForm=uploadform)

@app.route('/editHabit/<int:habit_id>', methods=['GET', 'POST'])
def edit_habit(habit_id):
    form = editHabitForm()
    habit = Habit.query.get(habit_id)
    if form.validate_on_submit():
        habit.name = form.name.data
        db.session.commit()
        flash('Your habit is updated.')
        return redirect(url_for('index'))
    form.name.data = habit.name
    return render_template('editHabit.html', form=form)

@app.route('/delHabit/<int:habit_id>', methods=['POST'])
def delHabit(habit_id):
    form = delHabitForm()
    if form.validate_on_submit():
        habit = Habit.query.get(habit_id)
        db.session.delete(habit)
        db.session.commit()
        flash('the habit is deleted')
    else:
        print('del failed')
        abort(400)
    return redirect(url_for('index'))

