from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SelectField, PasswordField, BooleanField, IntegerField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length,NumberRange, ValidationError, Email


def PasswordLength(form, field):
    if len(field.data) > 42 or len(field.data) < 8:
        raise ValidationError('The password not 22222')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[PasswordLength])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RecordForm(FlaskForm):
    submit = SubmitField('Submit')


class UploadForm(FlaskForm):
    photo = FileField('uploadIMG',
                      validators=[
                          FileRequired(),
                          FileAllowed(['txt', 'png', 'css', 'jpg', 'JPG'])
                      ])
    submit = SubmitField('Upload')


class AddHabitForm(FlaskForm):
    name = StringField('Habit', validators=[DataRequired()])
    categorys = ['Career', 'Finance', 'Social', 'Family', 'Health', 'Growth', 'Funny', 'Study']
    choice = []
    for cat in categorys:
        choice.append((cat, cat))


    category_name = SelectField('Category', choices=choice)
    # category = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    done_value = IntegerField('Score When Done', validators=[NumberRange(0, 100)])
    undone_value = IntegerField('Score without Done', validators=[NumberRange(0, 100)])
    submit = SubmitField('ADD')


class EditHabitForm(AddHabitForm):
    submit = SubmitField('Update')


class DelHabitForm(FlaskForm):
    submit = SubmitField('Delete')