from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from momentjs import momentjs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['WHOOSH_BASE'] = os.path.join(basedir, 'search.db')
app.config['CSRF_ENABLED'] = True
app.secret_key = '12AvdfGFHDdfvSDHFF4!76#$%7'
db = SQLAlchemy(app)
app.jinja_env.globals['momentjs'] = momentjs