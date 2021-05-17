from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    firstname = StringField('First Name: ', validators=[DataRequired()])
    surname = StringField('Surname: ', validators=[DataRequired()])
    dob = DateField('Date of Birth: ', format='%Y-%m-%d')
    address = StringField('Address: ')
    country = StringField('Country: ')
    state = StringField('State: ')
    postcode = IntegerField('Postcode: ')
    phone = IntegerField('Phone: ')
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Register')

class CreateQuizForm(FlaskForm):
    title = StringField('Title: ', validators=[DataRequired()])
    sport = StringField('Sport: ', validators=[DataRequired()])
    submit = SubmitField('Create Quiz')

class CreateQuestionForm(FlaskForm):
    question = StringField('Question: ', validators=[DataRequired()])
    answer = StringField('Answer: ', validators=[DataRequired()])
    submit = SubmitField('Add Question')