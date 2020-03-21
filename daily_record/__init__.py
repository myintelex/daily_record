import os

import click
from flask import Flask, jsonify 
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# from daily_record import  models, views, commands
from daily_record.blueprints.index import index_bp
from daily_record.blueprints.habit import habit_bp 
from daily_record.blueprints.charts import charts_bp 
from daily_record.setting import config
from daily_record.extensions import db, bootstrap
from daily_record.fake import fake_data
from daily_record.models import Category

def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('daily_record')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    # register_errors(app)
    # register_template_context(app)
    return app


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)

def register_blueprints(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(habit_bp)
    app.register_blueprint(charts_bp)

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
        categorys = [
            'Career', 'Finance', 'Social', 'Family', 'Health', 'Growth', 'Funny',
            'Study'
        ]
        for cate in categorys:
            category = Category(name=cate)
            db.session.add(category)
        db.session.commit()
        click.echo('Initialized the categorys.')

    @app.cli.command()
    def fake():
        fake_data()
        click.echo('Initialized database.')