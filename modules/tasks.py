from flask import Flask, render_template, request, redirect, session, Blueprint
from models.models import User, Task
from extensions import db

task_blueprint = Blueprint('task', __name__)

@task_blueprint.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if 'username' in session:
        username = session['username']
        users= User.query.all()

        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            assigned_to = request.form['assigned_to']
            task = Task(name=name, description=description, assigned_to=assigned_to)
            db.session.add(task)
            db.session.commit()
            return redirect('/dashboard')
        return render_template('add_task.html', username=username, users=users)
    return redirect('/login')

@task_blueprint.route('/delete_task/<int:id>')
def delete_task(id):
    if 'username' in session:
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return redirect('/dashboard')
    return redirect('/login')


# Define a route for Complete a task
@task_blueprint.route('/complete_task/<int:id>')
def complete_task(id):
    if 'username' in session:
        task = Task.query.get_or_404(id)
        task.completed = True
        db.session.commit()
        return redirect('/dashboard')
    return redirect('/login')
