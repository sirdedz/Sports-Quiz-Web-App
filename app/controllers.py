from app import forms, models, db, app
from flask import render_template, flash, redirect, request, url_for, session
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Quiz, Question, Result


class UserController():

    def login(form):

        return render_template('login.html', title='Login', form=form)
    
    def login_post(form):

        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('user'))


    def logout():
        logout_user()
        return redirect(url_for('index'))


    def register(form):

        users = User.query.all()

        return render_template('register.html', title='Register', users=users, form=form)

    def register_post(form):

        username = request.form.get('username')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        surname = request.form.get('surname')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        #user will return not None if a user with that username already exists
        if user:
            flash('Username is already in use')
            return redirect(url_for('register'))

        #otherwise create a new database entry
        new_user = User(username=username, email=email, firstname=firstname, surname=surname)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))


class QuizController():
    def create(form):

        title = request.form.get('title')
        sport = request.form.get('sport')

        quiz = Quiz.query.filter_by(title=title).first()

        if quiz:
            flash('Quiz already exists, add questions:')
            return redirect(url_for('create_question', quiz_title=title))

        new_quiz = Quiz(title=title, sport=sport)
        db.session.add(new_quiz)
        db.session.commit()

        return redirect(url_for('create_question', quiz_title=title))

    def createQuestion(form, quiz_title):

        quiz = Quiz.query.filter_by(title=quiz_title).first()

        question = request.form.get('question')
        answer = request.form.get('answer')

        new_question = Question(question=question, answer=answer, quiz_id=quiz.id)

        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for('create_question', quiz_title=quiz_title))
