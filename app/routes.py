from app import app, db, models, forms
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app.controllers import UserController, QuizController
from werkzeug.urls import url_parse

from app.models import User, Quiz, Question

@app.route('/')
@app.route('/index')
def index():

    #Get quizzes for front page
    quizzes = Quiz.query.all()

    return render_template('index.html', quizzes=quizzes)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if not current_user.is_authenticated:
        if form.validate_on_submit():
            UserController.login_post(form)

        return UserController.login(form)


    return redirect(url_for('user'))

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
@login_required
def quiz():
    quiz_title = session.get('quiz', None)
    quiz = Quiz.query.filter_by(title=quiz_title).first()

    return render_template('quiz.html', title="Quiz", quiz=quiz)

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

@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if current_user.username == 'admin':

        form = forms.CreateQuizForm()

        if form.validate_on_submit():
            return QuizController.create(form)

        return render_template('create_quiz.html', title="Create A Quiz", form=form)
    else:
        return redirect('index')

@app.route('/create_question', methods=['GET', 'POST'])
@login_required
def create_question():
    if current_user.username == 'admin':

        form = forms.CreateQuestionForm()

        quiz = session.get('quiz', None)

        quiz_object = Quiz.query.filter_by(title=quiz).first()
        quiz_id = quiz_object.id

        questions = Question.query.filter(Question.quiz_id==quiz_id).all()

        if form.validate_on_submit():
            return QuizController.createQuestion(form, quiz_id)

        return render_template('create_question.html', title="Create A Question", form=form, questions=questions)
    else:
        return redirect('index')


@app.route('/delete_quiz', methods=['GET', 'POST'])
@login_required
def delete_quiz():
    if current_user.username == 'admin':
        quiz = session.get('quiz', None)

        quiz_object = Quiz.query.filter_by(title=quiz).first()
        
        db.session.delete(quiz_object)
        db.session.commit()

    
    return redirect('index')

