from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import getcwd


app = Flask(__name__)
app.secret_key = open(getcwd() + "\\secret").read()
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////%s//main.sqlite3' % getcwd()[3:].replace('\\', '//')
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from mer import routes, models, files
