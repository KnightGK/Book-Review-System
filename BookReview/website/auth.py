from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flaskext.mysql import MySQL
from .model import Operator, Reader
from . import db
from . import users

from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        print("trying to login")
        print(name)
        print(password)

        userO = Operator.query.filter_by(name=name).first()
        userR = Reader.query.filter_by(ReaderName=name).first()

        if userO:
            if check_password_hash(userO.password, password):
                login_user(userO, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash("Incorret password!", category='error')
        else:
            if userR.ReaderPassword == password:
                login_user(userR, remember=True)
                return redirect(url_for('views.userdash'))

    return render_template("main.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST':  # retrieving user info from sign up
        id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        # returning the first entry with the email
        user = Operator.query.filter_by(name=name).first()
        if user:
            msg = 'ID alread exsit'
        elif password != passwordConfirm:
            msg = 'Password dont match'
        elif len(password) < 8 or len(password) > 50:
            msg = 'Please make the password between 8 and 50 character'
        else:
            msg = 'Created Account'
            newUser = Operator(id=id, name=name, password=generate_password_hash(
                password, method="sha256"))
            print(id, name, password)
            db.session.add(newUser)
            db.session.commit()
            # log in user after they successfully created their account
            login_user(newUser, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.dashboard'))

    return render_template("signup.html", user=current_user, mssg=msg)