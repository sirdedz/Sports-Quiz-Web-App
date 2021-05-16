from app import app, db, models, forms
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.controllers import UserController
from werkzeug.urls import url_parse

from app.models import User, Account, Offer, Event

@app.route('/')
@app.route('/index')
def index():

    #Get events for front page
    events = Event.query.all()

    return render_template('index.html', events=events)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if not current_user.is_authenticated:
        if form.validate_on_submit():
            UserController.login_post(form)

        return UserController.login(form)


    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    return UserController.logout()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()

    if form.validate_on_submit():
        return UserController.register_post(form)

    return UserController.register(form)


@app.route('/quiz')
def quiz():
    return render_template('quiz.html', title="Quiz")

@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    return render_template('user.html', title="Account")

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title="About Us")

@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html', title="Your Results")

@app.route('/content', methods=['GET', 'POST'])
def content():
    return render_template('content.html', title="Learning Materials")

@app.route('/stats', methods=['GET'])
def stats():
    return render_template('stats.html', title="Global Statistics")
