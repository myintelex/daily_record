import click

from daily_record import app, db
from daily_record.fake import fake_data

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized the database.')

@app.cli.command()
def fake():
    fake_data()
    click.echo('Initialized database.')
