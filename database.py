from random import choice
import sqlite3
import datetime
import sys


BASIC_STDOUT = sys.stdout
INFO_LOG_FILE = "asd.txt"
LOGGER_FILE = "log.txt"
ERROR_LOG_FILE = "errors.txt"


def logger(func):
    def __wrapper(*args, **kwargs):
        code = func(*args, **kwargs)
        if code:
            printError(f"Error occurred in function {func.__name__}", to_file=True)

    return __wrapper


def printError(info, to_file=False):
    if to_file:
        sys.stdout = open(ERROR_LOG_FILE, "a")
    print(f'[ERROR][{datetime.datetime.today():%d.%m.%Y-%H:%M:%S}]\t{info}')
    if to_file:
        sys.stdout = BASIC_STDOUT
    return 0


def printInfo(info):
    sys.stdout = open(INFO_LOG_FILE, "a")
    print(f'[INFO][{datetime.datetime.today():%d.%m.%Y-%H:%M:%S}]\t{info}')
    sys.stdout = BASIC_STDOUT


class dataBase:
    def __init__(self):
        from string import digits, ascii_letters
        self.alphabet = ascii_letters + digits
        self.__connect_to_database()
        self.__connect_to_login()
        self.__connect_to_users()
        self.__connect_to_testes()

    @logger
    def __connect_to_database(self):
        try:
            printInfo("Starting")
            self.main = sqlite3.connect("main.bd")
            self.cursor = self.main.cursor()
        except:
            printInfo("Failed to connect to database")
            return -1
        return 0

    @logger
    def __connect_to_login(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS login(login, psw, salt)")
        except sqlite3.OperationalError:
            printInfo("Failed to create 'login'")
            return -1
        return 0

    @logger
    def __connect_to_users(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users(login, name, surname, middle_name, total)")
        except sqlite3.OperationalError:
            printInfo("Failed to create 'users'")
            return -1
        return 0

    @logger
    def __connect_to_testes(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS testes(login, test_id, score)")
        except sqlite3.OperationalError:
            printInfo("Failed to create 'testes'")
            return -1
        return 0

    def __random_salt(self):
        return "".join(choice(self.alphabet) for _ in range(16))

    def __user_exists(self, login):
        exists = self.cursor.execute(f"SELECT * FROM users WHERE login='{login}'").fetchall()
        if not exists:
            return False
        return True

    @logger
    def test_completion(self, login, test_id, score, force=False):
        printInfo(f"Attempting to validate '{login}' score for test {test_id}")
        if not self.__user_exists(login):
            printInfo(f"There is no user '{login}'")
            return -1
        res = self.cursor.execute(f"SELECT * FROM testes WHERE login='{login}' AND test_id='{test_id}'").fetchall()
        if res:
            if int(score) > res[0][-1] or force:
                self.cursor.execute(f"UPDATE testes SET score={score} WHERE login='{login}' and test_id='{test_id}'")
                self.main.commit()
                printInfo(f"Updated score for '{login}' on test {test_id} to {score}")
            else:
                printInfo(f"'{login}' has better score on {test_id}, not updating")
        else:
            self.cursor.execute(f"INSERT INTO testes(login, test_id, score) values('{login}', '{test_id}', {score})")
            self.main.commit()
            printInfo(f"Set score for '{login}' on test {test_id} to {score}")
        self.update_score(login)
        return 0

    @logger
    def update_score(self, login):
        if not self.__user_exists(login):
            print(f"Error in users: either there is more than one '{login}' either there is no '{login}'")
            return -1
        res = self.cursor.execute(f"SELECT * FROM testes WHERE login='{login}'").fetchall()
        to_update = 0
        if res:
            to_update += sum([i[2] for i in res])
        self.cursor.execute(f"UPDATE users SET total={to_update} WHERE login='{login}'")
        self.main.commit()
        printInfo(f"Updated score for '{login}'")
        return 0


    @logger
    def add_user(self, login, psw, name, surname="", middle_name=""):
        printInfo(f"Creating user '{login}'...")
        if self.__user_exists(login):
            printInfo(f"user '{login}' already exists")
        self.cursor.execute(f"INSERT INTO users(login, name, surname, middle_name, total) "
                            f"values('{login}', '{name}', '{surname}', '{middle_name}', 0)")
        salt = self.__random_salt()
        self.cursor.execute(f"INSERT INTO login(login, psw, salt) values('{login}', '{hash(psw + salt)}', '{salt}')")
        self.main.commit()
        printInfo(f"Created user '{login}'...")
        return 0

    def print_info(self, login):
        return self.cursor.execute(f"SELECT * FROM users WHERE login='{login}'").fetchall()[0]


a = dataBase()

a.test_completion("1", "1", "50")

a.add_user(login="example", psw="QWERTY", name="example", surname="example", middle_name="example")

a.test_completion("example", "first_test", "50")
a.update_score(login="example")
print(a.print_info(login="example"))

a.test_completion("example", "first_test", "100")
a.update_score(login="example")
print(a.print_info(login="example"))

a.test_completion("example", "first_test", "60")
print(a.print_info(login="example"))

a.test_completion("example", "second_test", "70")
print(a.print_info(login="example"))