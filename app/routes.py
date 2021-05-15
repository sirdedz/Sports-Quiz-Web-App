from app import app, db, models
from flask import render_template, flash, redirect
from app import forms

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

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')

    return render_template('login.html', title="Sign In", form=form)


@app.route('/register')
def register():
    return "Placeholder for registration page"


@app.route('/quiz')
def quiz():
    return render_template('quiz.html', title="Quiz")

@app.route('/user', methods=['GET', 'POST'])
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
    return render_template('stats.html' title="Global Statistics")
