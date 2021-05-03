from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    dob = db.Column(db.DateTime)
    address = db.Column(db.String(128))
    country = db.Column(db.String(64))
    state = db.Column(db.String(64))
    postcode = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))

    account = db.relationship('Account')
    offers = db.relationship('Offer')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
        return '<Account {}>'.format(self.user_id)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(128))

    offers = db.relationship('Offer')

    def __repr__(self):
        return '<Event {}>'.format(self.title)

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    odds = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('Event.id'))