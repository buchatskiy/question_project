# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, request, redirect, flash, session
from models import User, Question, Answer
from wtforms import Form, TextField, PasswordField, validators
from app import db, app
from sqlalchemy import desc
from flask.ext.login import (LoginManager, login_required, login_user, logout_user, current_user)
from momentjs import momentjs


app.jinja_env.globals['momentjs'] = momentjs
login_manager = LoginManager()
MAX_SEARCH_RESULTS = 10

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

login_manager.init_app(app)

@app.route('/')
def main():
    questions=Question.query.order_by(desc(Question.pub_date))
    answers_query=Answer.query
    return render_template('base.html', questions=questions, answers_query=answers_query)

@app.route('/add_question', methods=['POST'])
def add_entry():
    if request.form['new_question']:
        db.session.add(Question(request.form['new_question'], User.query.filter_by(username=current_user.username).first()))
        db.session.commit()
    return redirect(url_for('main'))

@app.route('/add_answer=<int:question_id>', methods=['POST'])
def add_answer(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if request.form['new_answer']:
        db.session.add(Answer(request.form['new_answer'], question, User.query.filter_by(username=current_user.username).first()))
        db.session.commit()
    return redirect(url_for('show_question', question_id=question_id))


@app.route('/question=<int:question_id>')
def show_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    answers=Answer.query.filter_by(question_id=question_id)
    return render_template('question.html', question=question, answers=answers)


def my_email_check(form, field):
    if User.query.filter_by(email=field.data).first():
        raise validators.ValidationError(u'Користувач з таким емейлом уже зареєстрований')

def my_username_check(form, field):
    if User.query.filter_by(username=field.data).first():
        raise validators.ValidationError(u'Користувач з таким логіном уже зареєстрований')


class RegistrationForm(Form):
    username = TextField(u'Логін', [validators.Length(min=4, max=25, message=u'Поле має бути не менше 4 і не більше 25 символів.'), my_username_check])
    email = TextField(u'Email адрес', [validators.Email(message=u'Невірний email.'), my_email_check])
    password = PasswordField(u'Пароль', [
        validators.Required(message=u"Обов'язкове поле."),
        validators.EqualTo('confirm', message=u'Пароль повинен співпадати')
    ])
    confirm = PasswordField(u'Повторіть пароль ще раз')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

class LoginForm(Form):
    username = TextField(u'Логін', [validators.Required(message=u"Обов'язкове поле.")])
    password = PasswordField(u'Пароль', [validators.Required(message=u"Обов'язкове поле.")])

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = {}
    username = ""
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            error['username'] = u'Неправильний логін'
        else:
            username = request.form['username']
            for u in User.query.filter_by(username=request.form['username']):
                if u.password != request.form['password']:
                    error['password'] = u'Неправильний пароль'
                else:
                    login_user(user)
                    return redirect(url_for('main'))
    return render_template('login.html', username=username, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('main'))


class SearchForm(Form):
    search = TextField(u'Шукати:', [validators.Required(message=u"Обов'язкове поле.")])

@app.route('/search', methods = ['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('search_results', query = form.search.data))
    return render_template('search.html', form=form)

@app.route('/search_results/<query>')
def search_results(query):
    results = Question.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
        query = query,
        results = results)

if __name__ == '__main__':
    app.run(debug=True)