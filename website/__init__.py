from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .dbops import DB
from flask_bootstrap import Bootstrap

db = DB()

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'very secret'

from .views import views
from .auth  import auth
from .admin import admin

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(admin, url_prefix='/')




