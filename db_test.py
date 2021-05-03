from app import db
from app.models import User

u = User(username="JohnDoe123", email='johndoe123@gmail.com')
db.session.add(u)
db.session.commit()


users = User.query.all()

for u in users:
    print(u.id, u.username, u.email)