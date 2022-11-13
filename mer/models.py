from flask_login import UserMixin

from mer import db


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True, nullable=False)
    psw = db.Column(db.String(1024), nullable=False)


class Info(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), db.ForeignKey('user.login'), unique=True, nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20), nullable=True)
    course = db.Column(db.Integer, nullable=False)


class TestResults(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), db.ForeignKey('user.login'), nullable=False)
    course = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    test_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=True)


class Courses(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(40), nullable=False)


db.create_all()