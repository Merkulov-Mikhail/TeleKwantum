from mer import db
from mer.models import Courses


N = input("Введите имя курса\n>")
while N != "exit":
    validation = input(f"Подтвердите создание курса {N} (Y/N(Да или нет))")
    if validation.lower() == "y":
        new = Courses(course_name=N)
        db.session.add(new)
        db.session.commit()
        print("Курс добавлен")
    N = input("Введите имя курса\n>")
