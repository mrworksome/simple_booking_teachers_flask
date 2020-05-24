import json
import random

from flask import render_template, request

from application import db
from application.forms import BookingForm, RequestForm
from application.models import Teacher, Goal, Booking, Request
from flask import current_app as app

# def get_goals():
#     goals = dict()
#     for goal in db.session.query(Goal).all():
#         if len(goals) <= 4:  # 4 may be variable for main page's limit of goals
#             goals[goal.goal_url] = goal.goal_name
#         else:
#             break
#     return goals
from application.utils import get_goals


@app.route('/')
def main_page():
    teachers = db.session.query(Teacher).all()
    teach_s = random.sample(teachers, 6)
    goals = get_goals()
    return render_template('index.html',
                           teachers=teach_s,
                           goals=goals
                           )


@app.route('/tutors/')
def teachers_all():
    teachers = db.session.query(Teacher).all()
    goals = get_goals()
    return render_template('index.html',
                           teachers=teachers,
                           title='Все репетиторы',
                           goals=goals
                           )


days_name = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг",
             "fri": "Пятница",
             "sat": "Суббота", "sun": "Воскресенье"}


@app.route('/profiles/<int:teacher_id>')
def get_teacher(teacher_id):
    teacher = db.session.query(Teacher).get(teacher_id)
    if teacher:
        goals = db.session.query(Goal).filter(Goal.g_id == teacher_id).all()
        goals_teacher = []
        for i in goals:
            goals_teacher.append(i.goal_name)
        free_dict = json.loads(teacher.free)

        return render_template('profile.html',
                               title=teacher.name,
                               teacher_dict=teacher,
                               goals=goals_teacher,
                               free=free_dict,
                               days_name=days_name
                               )


@app.route('/goals/<goal>/')
def get_goal(goal):
    teachers_for_goal = db.session.query(Goal).filter(Goal.goal_url == goal).all()
    teachers = []
    for teacher in teachers_for_goal:
        teachers.append(db.session.query(Teacher).get(teacher.teacher_id))
    goal_name = db.session.query(Goal).filter(Goal.goal_url == goal).first().goal_name
    return render_template('goal.html',
                           teachers=teachers,
                           goal=goal_name
                           )


@app.route('/booking/<int:teacher_id>/<day>/<b_time>/')
def do_the_booking(teacher_id, day, b_time):
    day_ru = days_name[day]
    form = BookingForm(
        client_weekday=day,
        client_time=b_time,
        teacher_id=teacher_id
    )
    teacher = db.session.query(Teacher).get(teacher_id)
    return render_template('booking.html',
                           teacher_dict=teacher,
                           title='Забронировать время у преподавателя',
                           form=form,
                           day_ru=day_ru
                           )


@app.route('/booking_done/', methods=['POST', 'GET'])
def booking_done():
    if request.method == 'POST':
        form = BookingForm()
        day_ru = days_name[form.client_weekday.data]
        if form.validate():
            book = Booking()
            form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            return render_template('booking_done.html',
                                   day_ru=day_ru,
                                   info=form,
                                   title='Время у преподователя забранированно'
                                   )

        else:
            return "Форма получена, но есть ошибки!"
    else:
        return "Кажется, форма не отправлена!"


@app.route('/request/')
def do_request():
    form = RequestForm()
    return render_template('request.html',
                           title='Заявка на подбор',
                           form=form
                           )


@app.route('/request_done/', methods=['POST', 'GET'])
def request_done():
    if request.method == 'POST':
        form = RequestForm()
        goal = get_goals()[form.client_goal.data]
        if form.validate():
            write_req = Request()
            form.populate_obj(write_req)
            db.session.add(write_req)
            db.session.commit()
            return render_template('request_done.html',
                                   goal=goal,
                                   form=form,
                                   title=f'Заявка создана, {form.client_name}'
                                   )
    else:
        return "Кажется, форма не отправлена!"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Страница не найдена'), 404
