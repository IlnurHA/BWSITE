from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LobbyForm(FlaskForm):
    map = StringField('Карта', validators=[DataRequired()])
    size = IntegerField('Количество игроков', validators=[DataRequired()])
    submit = SubmitField('Создать лобби')
