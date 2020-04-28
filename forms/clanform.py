from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ClanForm(FlaskForm):
    name = StringField('Название клана', validators=[DataRequired()])
    short_name = StringField('Короткое название клана')
    submit = SubmitField('Создать клан')
