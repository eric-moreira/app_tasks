from flask import render_template, request, redirect, session, Blueprint
from bcrypt import hashpw, gensalt, checkpw
import base64
from models.models import User, Task
from extensions import db



auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hash = hashpw(password.encode('utf-8'), gensalt())
        encoded_hash = base64.b64encode(hash).decode("utf-8")
        user = User(username=username, pwd=encoded_hash, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('signup.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect('/dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            hash = base64.b64decode(user.pwd)
            if checkpw(password.encode('utf-8'), hash):
                session['username'] = username
                return redirect('/dashboard')
        return redirect('/login')
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@auth_blueprint.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        tasks = Task.query.filter_by(assigned_to=user.id).all()
        return render_template('dashboard.html', username=username, tasks=tasks)
    return redirect('/login')
