from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from files import test_data, videos
from mer import app, login_manager, db
from models import User, Info, TestResults

BASIC_POINTS_MULTIPLIER = 1


@login_manager.user_loader
def load(id):
    return User.query.get(id)


@app.route('/video/<int:video_id>', methods=['GET'])
@login_required
def video(video_id):
    user_info = Info.query.get(current_user.id)
    if video_id >= len(videos[str(user_info.course)]):
        return render_template("video.html", video="-1")
    return render_template("video.html", video=videos[str(user_info.course)][video_id])


@app.route('/', methods=['GET'])
def hello_world():
    return redirect("/main")


@app.route('/main', methods=['GET'])
@login_required
def main():
    user_info = Info.query.get(current_user.id)
    if not user_info:
        flash("Данный пользователь отсутствует в базе данных")
        return redirect("/login")
    statuses = []
    dat = test_data[str(user_info.course)]
    for test in dat.keys():
        ans = TestResults.query.filter_by(login=user_info.login, test_id=test).first()
        if not ans:
            statuses.append(-1)  # -1 - пользователь не делал тест
        else:
            statuses.append(ans.score)  # кол-во баллов, набранных пользователем за тест
    return render_main()


def load_table():
    dat = {}
    for test_result in TestResults.query.all():
        if test_result.login not in dat:
            dat[test_result.login] = 0
        dat[test_result.login] += test_result.score
    to_return = []
    for usr in dat.keys():
        user = Info.query.filter_by(login=usr).first()
        to_return.append((f"{user.surname} {user.name} {user.middle_name if user.middle_name else ''}", dat[usr]))
    return sorted(to_return, key=lambda x: x[1], reverse=True)


@app.route('/test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def test(test_id):
    dat = test_data[str(Info.query.get(current_user.id).course)][str(test_id)]
    if not list(request.form.values()):
        return render_template("test.html", questions=dat["questions"], answers=dat["answers"])
    points = count_points(dat, current_user.id, request.form)
    user_info = Info.query.get(current_user.id)
    res = TestResults.query.filter_by(login=user_info.login, course=user_info.course, test_id=test_id).first()
    if res:
        res.score = max(res.score, points)
    else:
        res = TestResults(login=user_info.login, course=user_info.course, test_id=test_id, score=points)
        db.session.add(res)
    db.session.commit()
    return redirect('/main')


def render_main():
    user_info = Info.query.get(current_user.id)
    videos_data = [vd[:vd.rfind(".")] for vd in videos[str(user_info.course)]]
    table = load_table()
    return render_template('main.html',
                           na=user_info.name,  # Строка для привествия с пользователем
                           data=test_data[str(user_info.course)],  # Список тестов пользователя
                           videos=videos_data,  # Список видео пользователя
                           table=table)  # Таблица результатов


def count_points(values: dict, user_id, user_answers):
    questions = values["questions"]
    answers = values["answers"]
    right_answers = values["right_answers"]
    type = values["type"]
    points = 0
    for form_id in range(len(questions)):
        ans = user_answers.get(f"{form_id}")
        if ans is None:
            continue
        user_answer = answers[form_id].split(';')[int(ans)]
        if normalize(user_answer) == normalize(right_answers[form_id]):
            points += BASIC_POINTS_MULTIPLIER * int(type)
    return points


def normalize(n: str):
    return n.strip().lower()


@app.route('/add_message', methods=['POST'])
@login_required
def add_message():
    return redirect(url_for('main'))


@app.route("/login", methods=["GET", "POST"])
def login():
    login, psw = request.form.get("login"), request.form.get("password")
    if login and psw:
        usr = User.query.filter_by(login=login).first()
        if usr:
            if check_password_hash(usr.psw, psw):
                login_user(usr)
                return redirect(url_for('main'))
        flash("Логин или пароль некорректны")
    else:
        flash("Заполните поля логина и пароля")
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.after_request
def redirect_to_signin(response):
    if 401 == response.status_code:
        return redirect(url_for("login"))
    return response
