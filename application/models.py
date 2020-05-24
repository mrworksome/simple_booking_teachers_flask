from . import db


class Teacher(db.Model):
    __tablename__ = 'teachers'
    t_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.relationship("Goal", back_populates="teacher")
    free = db.Column(db.String, nullable=False)
    bookings = db.relationship("Booking", back_populates="teacher")


class Goal(db.Model):
    __tablename__ = 'goals'
    g_id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String, nullable=False)
    goal_url = db.Column(db.String, nullable=False)
    teacher = db.relationship("Teacher", back_populates="goals")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.t_id"))


class Booking(db.Model):
    __tablename__ = 'bookings'
    b_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String, nullable=False)
    client_weekday = db.Column(db.String, nullable=False)
    client_time = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.t_id"))
    teacher = db.relationship("Teacher", back_populates="bookings")


class Request(db.Model):
    __tablename__ = 'requests'
    r_id = db.Column(db.Integer, primary_key=True)
    client_goal = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String, nullable=False)
    free_time = db.Column(db.String, nullable=False)
