from werkzeug.security import generate_password_hash

from mer import db
from mer.models import User


N = input("Введите логин пользователя, пароль и подтверждение пароля (exit - прекратить работу) черрез пробел\n>")
while N != "exit":
    a = N.split()
    if len(a) != 3:
        N = input("Некорректные данные\n>")
        continue
    if a[1] == a[2]:
        new_user = User(login=a[0], psw=generate_password_hash(a[1]))
        db.session.add(new_user)
        db.session.commit()
        print("Пользователь добавлен")
    N = input("\n>")