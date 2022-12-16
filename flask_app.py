import os

from flask import Flask, render_template, flash, redirect, url_for, session, request, jsonify
from flask_login import LoginManager, login_required, login_user, UserMixin, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

from services.forms import login_form, task_form, task_edit_form, registration_form


# app = Flask(__name__)

# app.config['SECRET_KEY'] = '022478f43dd6b249e1fd271d0f049de1'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["SESSION_PERMANENT"] = False
# db = SQLAlchemy(app)

# login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = 'index'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '022478f43dd6b249e1fd271d0f049de1'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SESSION_PERMANENT"] = False
    return app


def db_create(app):
    db = SQLAlchemy(app)
    db.init_app(app)
    return db


def login_manager_create(app):
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'index'
    return login_manager


app = create_app()
db = db_create(app)
login_manager = login_manager_create(app)



BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ...
    # Since SQLAlchemy 1.4.x has removed support for the 'postgres://' URI scheme,
    # update the URI to the postgres database to use the supported 'postgresql://' scheme
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'instance', 'main.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Logging
    LOG_WITH_GUNICORN = os.getenv('LOG_WITH_GUNICORN', default=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Class to create a user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"


# Class to create a task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    priority = db.Column(db.String(255))
    status = db.Column(db.Integer)
    todo_owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Task {self.task_name} {self.priority} {self.status} {self.todo_owner}'


# Run index.html page
# main / login page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = login_form.AuthorisationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            session['username'] = form.username.data
            session['password'] = form.password.data
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, session['password']):
                flash('You were successfully logged in', 'login_success')

                login_user(user)
                return redirect(url_for('main'))

            else:
                flash('Invalid username or password', 'login_error')

    return render_template('index.html', form=form)


# Run main.html page
# Contains buttons which are used to add, edit and delete tasks
@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    currentTasks = Task.query.filter_by(todo_owner=current_user.id).all()
    if request.method == 'POST':
        if request.form['manage_task'] == 'delete':
            button_delete()
            return redirect(url_for('main'))
        elif request.form['manage_task'] == 'edit':
            id = request.form['task_id']
            return redirect(url_for('edit', task_id=id))
        elif request.form['manage_task'] == 'success':
            button_done()
            return redirect(url_for('main'))

    return render_template('main.html', tasks=currentTasks)


# Create new task page
# Using forms and db to create new task
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = task_form.TodoForm()
    if request.method == 'GET':
        return render_template('create.html', form=form)
    if request.method == 'POST':
        task = Task(task_name=form.task_name.data, priority=form.priority.data, status=0,
                    todo_owner=current_user.id)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('main'))
        except:
            flash('Task has been created', 'task_created')
            return redirect(url_for('main'))
    return render_template('create.html', form=form)


# Edit page
# Get data from task db and edit it
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    form = task_edit_form.EditTaskForm()
    task = Task.query.filter_by(id=task_id).first()

    if request.method == 'GET':
        form.task_name.data = task.task_name
        form.priority.data = task.priority
        return render_template('edit.html', form=form)
    if request.method == 'POST':
        task.task_name = form.task_name.data
        task.priority = form.priority.data
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('edit.html', form=form, task_id=task_id)


# Create json file of tasks
# Get data from user and task dbs
@app.route('/json', methods=['GET', 'POST'])
@login_required
def json():
    tasks = Task.query.filter_by(todo_owner=current_user.id).all()
    user = User.query.filter_by(id=current_user.id).first()

    tasks_list = []

    for task in tasks:
        if task.status == 0:
            status = 'Not done'
        else:
            status = 'Done'
        tasks_list.append({
            'task_owner': user.username,
            'task_name': task.task_name,
            'priority': task.priority,
            'status': task.status,
            'status_name': status
        })
    return jsonify(tasks_list), {'Content-Type': 'application/json'}


# Registration page
# Using flask_wtf forms
# Using sessions to store data
# Using werkzeug.security to hash password
@app.route('/registration', methods=['POST', 'GET'])
@login_required
def registration():
    form = registration_form.AuthorisationForm()
    if request.method == 'POST':
        session['username'] = form.username.data
        session['password'] = form.password.data
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('User already exists', 'user_exists')
            return redirect(url_for('index'))
        else:
            new_user = User(username=form.username.data,
                            password=generate_password_hash(form.password.data, method='sha256'))
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('index'))
            except:
                return 'There was an issue adding your task'
    return render_template('registration.html', form=form)


# Simple logout function
# Using flask_login
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Manage completed tasks
def button_done():
    id = request.form['task_id']
    task = Task.query.filter_by(id=id).first()
    task.status = 1
    try:
        db.session.commit()
        return redirect(url_for('main'))
    except:
        return 'There was a problem updating that task'


# Manage deleted tasks
def button_delete():
    id = request.form['task_id']
    task = Task.query.filter_by(id=id).first()
    try:
        db.session.delete(task)
        db.session.commit()
    except:
        return 'There was a problem deleting that task'


if __name__ == '__main__':
    create_app()
