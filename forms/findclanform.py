from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class FindClanForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    submit = SubmitField('Поиск')
