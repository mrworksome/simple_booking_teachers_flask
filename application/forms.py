from flask_wtf import FlaskForm

from wtforms import StringField, HiddenField, RadioField
from wtforms.validators import InputRequired, Length

from application.utils import get_goals


class BookingForm(FlaskForm):
    client_name = StringField('Вас зовут', [InputRequired(message="Введите имя!"),
                                            Length(min=1, message="Слишком короткая строка")])
    client_phone = StringField('Ваш телефон', [InputRequired(message="Введите телефон!"),
                                               Length(min=1, message="Слишком короткая строка")])
    client_weekday = HiddenField("day")
    client_time = HiddenField("time")
    teacher_id = HiddenField("teacher_id")


class RequestForm(FlaskForm):
    client_name = StringField('Вас зовут', [InputRequired(message="Введите имя!"),
                                            Length(min=1, message="Слишком короткая строка")])
    client_phone = StringField('Ваш телефон', [InputRequired(message="Введите телефон!"),
                                               Length(min=1, message="Слишком короткая строка")])
    goals = []
    for key, value in get_goals().items():
        goals.append((key, value))
    client_goal = RadioField('Какая цель ваших занятий?', choices=goals)
    free_time = RadioField('Сколько свободного времени у вас есть?',
                           choices=[("1-2", "1-2 часа в неделю"), ("3-5", "3-5 часов в неделю"),
                                    ("5-7", "5-7 часов в неделю"), ("7-10", "7-10 часов в неделю")])
