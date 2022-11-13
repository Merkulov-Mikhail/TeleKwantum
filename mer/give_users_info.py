from mer import db
from mer.models import Info, Courses


def collect_data():
    name = input("Введите имя\n>")
    while not name:
        name = input("Введите имя\n>")
    surname = input("Введите фамилию\n>")
    while not surname:
        surname = input("Введите фамилию\n>")
    middle_name = input("Введите отчество(если отсутствует - оставьте пустую строку)\n>")
    while True:
        course = get_int("Введите курс пользователя (число, exit - прекратить ввод)\n>")
        if course == "exit":
            return None
        if Courses.query.get(int(course)):
            course_name = Courses.query.get(int(course))
            break
    text = f"Пользователь\nКурс: {course_name.course_name}\nИмя: {name}\nФамилия: {surname}\n"
    if middle_name:
        text += f"Отчество: {middle_name}\n"
    text += "Будет создан. Подвердить(Y/N (Да или нет))\n>"
    validation = input(text)
    while validation.lower() not in ['y', 'n']:
        validation = input("Y/N(Да или нет)\n>")
    if validation.lower() == "y":
        return course, name, surname, middle_name
    return None


def get_int(text):
    a = input(text)
    while not a.isdigit() and a != "exit":
        a = input(text)
    return a


N = input("Введите логин пользователя\n>")
while N != "exit":
    ans = Info.query.filter_by(login=N).first()
    if ans:
        print("Введённый пользователь существует")
    else:
        dat = collect_data()
        if dat is None:
            print("Отмена операции")
        else:
            course, name, surname, middle_name = dat
            if middle_name:
                information = Info(login=N, name=name, surname=surname, course=course, middle_name=middle_name)
            else:
                information = Info(login=N, name=name, surname=surname, course=course)
            db.session.add(information)
            db.session.commit()
            print("Данные обновленны")
    N = input("Введите логин пользователя\n>")
