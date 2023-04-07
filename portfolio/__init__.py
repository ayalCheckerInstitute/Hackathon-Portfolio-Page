import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# db_info = {'host': 'localhost',
#            'database': 'bookstore',
#            'psw': '1234',
#            'user': 'postgres',
#            'port': ''}
# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'portfolio.db')
app.config['SECRET_KEY'] = '123456'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yisroelbaum8@gmail.com'
app.config['MAIL_PASSWORD'] = 'munddfmibuzpiqlb'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


portfolio = SQLAlchemy(app)
migrate = Migrate(app, portfolio)
mail = Mail(app)


from portfolio import models, routes