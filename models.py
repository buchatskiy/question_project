from app import db, app
from datetime import datetime
from flask.ext.login import UserMixin
import flask.ext.whooshalchemy as whooshalchemy

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Question(db.Model):
    __searchable__ = ['text']

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_user = db.relationship('User',
        backref=db.backref('users', lazy='dynamic'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, text, pub_user, pub_date=None):
        self.text = text
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_user = pub_user
        self.pub_date = pub_date

    def __repr__(self):
        return '<Question %r>' % self.text



class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_user = db.relationship('User',
        backref=db.backref('users2', lazy='dynamic'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question',
        backref=db.backref('questions', lazy='dynamic'))

    def __init__(self, text, question, pub_user, pub_date=None):
        self.text = text
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.pub_user = pub_user
        self.question = question

    def __repr__(self):
        return '<Answer %r>' % self.text

whooshalchemy.whoosh_index(app, Question)