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


@app.route('/event')
def event():
    return "Placeholder for event page"


#probably incorrect for user page
@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
