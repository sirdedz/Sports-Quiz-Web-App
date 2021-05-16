from app import app, db, models, forms
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app.controllers import UserController, QuizController
from werkzeug.urls import url_parse
from werkzeug.datastructures import ImmutableMultiDict

from app.models import User, Quiz, Question, Result

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


@app.route('/quiz/<string:title>', methods=['GET'])
@login_required
def quiz(title):

    quiz_title = title
    quiz = Quiz.query.filter_by(title=quiz_title).first()

    questions = Question.query.filter(Question.quiz_id==quiz.id).all()

    return render_template('quiz.html', title="Quiz", quiz=quiz, questions=questions)

@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():

    results = Result.query.filter(Result.user_id==current_user.id).all()

    return render_template('user.html', title="Account", results=results)

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


@app.route('/delete_quiz/<string:title>', methods=['GET', 'POST'])
@login_required
def delete_quiz(title):
    if current_user.username == 'admin':

        quiz_object = Quiz.query.filter_by(title=title).first()
        
        db.session.delete(quiz_object)
        db.session.commit()

    
    return redirect('/')


@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    #quiz_title = request.form['title']

    jsonResult = request.get_json(force=True)
    quiz_title = jsonResult[0]['title']

    #Get actual quiz answers from database
    quiz_object = Quiz.query.filter_by(title=quiz_title).first()

    marking_questions = Question.query.filter(Question.quiz_id==quiz_object.id).all()
    score = 0
    questions_answered = 0
    result = {}

    class Answer():
        def __init__(self, marker, user):
            self.marker = marker
            self.user = user

    for x in range(len(jsonResult)-1):
        if marking_questions[x].answer == jsonResult[x+1]['answer']:
            #Correct answer
            score += 1
        
        result[marking_questions[x].question] = Answer(marking_questions[x].answer, jsonResult[x+1]['answer'])
            
        questions_answered += 1



    new_result = Result(score=score, questions_answered=questions_answered, user_id=current_user.id, quiz_title=quiz_title)

    db.session.add(new_result)
    db.session.commit()

    return "placehold"

