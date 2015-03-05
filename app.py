from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from momentjs import momentjs
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
app.config['CSRF_ENABLED'] = True
app.secret_key = '12AvdfGFHDdfvSDHFF4!76#$%7'
db = SQLAlchemy(app)
app.jinja_env.globals['momentjs'] = momentjs

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

WHOOSH_ENABLED = os.environ.get('HEROKU') is None
