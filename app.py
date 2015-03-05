from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from momentjs import momentjs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
app.config['CSRF_ENABLED'] = True
app.secret_key = '12AvdfGFHDdfvSDHFF4!76#$%7'
db = SQLAlchemy(app)
app.jinja_env.globals['momentjs'] = momentjs
