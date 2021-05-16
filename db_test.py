from app import db
from app.models import User, Quiz, Question

u = User(username="JohnDoe123", email='johndoe123@gmail.com')
u2 = User(username="SamKent123", email='samk123@gmail.com')
db.session.add(u)
db.session.add(u2)
db.session.add(a)
db.session.add(a2)
db.session.commit()


users = User.query.all()

for u in users:
    print(u.id, u.username, u.email)