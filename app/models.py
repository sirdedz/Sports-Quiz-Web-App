from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    dob = db.Column(db.DateTime)
    address = db.Column(db.String(128))
    country = db.Column(db.String(64))
    state = db.Column(db.String(64))
    postcode = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    sport = db.Column(db.String(64))

    def __repr__(self):
        return '<Quiz {}>'.format(self.title)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256))
    answer = db.Column(db.String(256))
    sport = db.Column(db.String(64))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    def __repr__(self):
        return '<Question {}>'.format(self.question)