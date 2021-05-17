#structure and routing for the website
#routes pages forms and tables

from app import app, db, models, forms
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app.controllers import UserController, QuizController, ResultController, StatsController
from werkzeug.urls import url_parse
from werkzeug.datastructures import ImmutableMultiDict

from app.models import User, Quiz, Question, Result
from datetime import datetime
import json
import populate_db

#route first page as the index page
@app.route('/')
@app.route('/index')
def index():

    #Get quizzes for front page
    quizzes = Quiz.query.all()

    return render_template('index.html', quizzes=quizzes)


#sets login form on the page login.html
#redirects depending on login form validators
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if not current_user.is_authenticated:
        if form.validate_on_submit():
            UserController.login_post(form)

        return UserController.login(form)


    return redirect(url_for('user'))

#routes functionality for logging out the user
@app.route('/logout')
def logout():
    return UserController.logout()


#places RegistrationForm() on page register.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()

    if form.validate_on_submit():
        return UserController.register_post(form)

    return UserController.register(form)


#sets chosen quiz to render on quiz.html through quiz_title key
#also routes questions through quiz_id key
@app.route('/quiz/<string:title>', methods=['GET'])
@login_required
def quiz(title):

    quiz_title = title
    quiz = Quiz.query.filter_by(title=quiz_title).first()

    questions = Question.query.filter(Question.quiz_id==quiz.id).all()

    return render_template('quiz.html', title="Quiz", quiz=quiz, questions=questions)

#generates result controller for results page
@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    return ResultController.generate()

#functionality for receiving and storing results into table
#then show user final results on page
@app.route('/get_results_json')
def get_results_json():

    results = Result.query.filter(Result.user_id==current_user.id).all()
    final = []

    for r in results:
        percentage = (r.score / r.questions_answered) * 100
        final.append({percentage: r.date})

    return json.dumps(final, default=str)

#adds functionality for admin
#shows user results
@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    if current_user.username == 'admin':
        results = Question.query.all()

        return render_template('user.html', title="Results", results=results)

    return render_template('user.html', title="Results")

#render about page, no forms
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title="About Us")

#render content page
@app.route('/content', methods=['GET', 'POST'])
def content():
    return render_template('content.html', title="Learning Materials")

#get Statscontroller
@app.route('/stats', methods=['GET'])
def stats():
    return StatsController.get()

#generate quiz for admin
#must be logged in
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

#must be logged in
#admin functionality
#create quiz question and render through create_question.html
@app.route('/create_question/<string:quiz_title>', methods=['GET', 'POST'])
@login_required
def create_question(quiz_title):
    if current_user.username == 'admin':

        form = forms.CreateQuestionForm()

        quiz_object = Quiz.query.filter_by(title=quiz_title).first()
        quiz_id = quiz_object.id

        questions = Question.query.filter(Question.quiz_id==quiz_id).all()

        if form.validate_on_submit():
            return QuizController.createQuestion(form, quiz_title)

        return render_template('create_question.html', title="Create A Question", form=form, questions=questions, quiz_title=quiz_title)
    else:
        return redirect('index')

#admin function for removing a quiz from table/s
@app.route('/delete_quiz/<string:title>', methods=['GET', 'POST'])
@login_required
def delete_quiz(title):
    if current_user.username == 'admin':

        quiz_object = Quiz.query.filter_by(title=title).first()

        db.session.delete(quiz_object)
        db.session.commit()


    return redirect('/')

#must be logged in as user
#retrieve corresct answers and compare to the user's
#finalise user's score and store new_result
@app.route('/submit_quiz', methods=['GET', 'POST'])
@login_required
def submit_quiz():

    jsonResult = request.get_json(force=True)
    quiz_title = jsonResult[0]['title']

    #Get actual quiz answers from database for marking
    quiz_object = Quiz.query.filter_by(title=quiz_title).first()

    marking_questions = Question.query.filter(Question.quiz_id==quiz_object.id).all()
    score = 0
    questions_answered = 0
    result = {}

    for x in range(len(jsonResult)-1):
        m = marking_questions[x].answer.replace(" ", '').lower()
        u = jsonResult[x+1]['answer'].replace(" ", '').lower()

        if m == u:
            #Correct answer
            score += 1

        result[marking_questions[x].question] = [marking_questions[x].answer, jsonResult[x+1]['answer']]

        questions_answered += 1


    result['score'] = [score, questions_answered]
    new_result = Result(score=score, questions_answered=questions_answered, user_id=current_user.id, quiz_title=quiz_title, date=datetime.utcnow())

    db.session.add(new_result)
    db.session.commit()

    return json.dumps(result, default=str)

#used to populate data tables for testing
@app.route('/populate')
@login_required
def populate():
    if current_user.username == 'admin':
        populate_db.run(current_user.id)

    return redirect('index')
