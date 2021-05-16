# sharkstakesllc

logo: https://vectr.com/tmp/jdrmi8dsl/b199CiH8XW.jpg?width=1000&height=1415.5&select=d6Z7hRFbk,h4RZBQ5Akb,aFHme6dQr&quality=1&source=selection

2: https://vectr.com/tmp/a3ASCJXv0g/c3HjXNh4MX.svg?width=1920&height=875.06&select=b1cIS9FkaZ,baGc2ISQF&source=selection

Wireframes: https://cacoo.com/


(Fix later)
Instructions for running flask app:
1. FLASK_APP=sharkstakes.py
2. export SECRET_KEY='temp_key'

Setting up Database:
1. Run 'sqlite3 app.db'
2. Run '.tables'
3. Run '.quit'
4. Run 'flask shell'
5. Run 'from app import db'
6. Run 'from app.models import [All tables in model]"
7. Run 'db.create_all()'

Adding to Database:
1. Run 'flask shell'
2. from app import db
3. from app.models import User, Account, Offer, Event
4. u = User(username="fasdfa", email="dfads@gmail.com")
5. db.session.add(u)
6. db.session.commit()
