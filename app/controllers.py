from app import forms, models
from flask import render_template, flash, redirect
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required


class UserController():
    
    def login():
        form = forms.LoginForm()

        if form.validate_on_submit():
            if user is None or not user.check_password(form.password.data):
                flash('invalid username or password')
                return redirect(url_for('login'))

            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = 'index'

            return redirect(url_for(next_page))

        return render_template('login.html', title="Login", form=form)

    def logout():
        logout_user()
        return redirect(url_for('index'))

    def register():
        username = request.form.get('username')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        surname = request.form.get('surname')

        user = User.query.filter_by(username=username).first()

        #user will return not None if a user with that username already exists
        if user:
            return redirect(url_for('register'))

        #otherwise create a new database entry
        new_user = User(username=username, email=email, firstname=firstname, surname=surname)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))