from alayatodo import app, db
from flask import (
    redirect,
    render_template,
    request,
    flash
    )
from flask_login import current_user, login_user, logout_user, login_required
from alayatodo.models import User, Todo


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = f.read()
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash("There is no username [{}]".format(username))
        return redirect('/login')

    if password != user.password:
        flash("Password is incorrect")
        return redirect('/login')

    login_user(user)
    return redirect('/todo')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@login_required
def todos():
    todos = Todo.query.filter_by(user_id=current_user.id)
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    description = request.form.get('description')

    if not description:
        flash("Can't add description as blank")
        return redirect('/todo')

    todo = Todo(user_id=current_user.id, description=description)
    db.session.add(todo)
    db.session.commit()
    flash("New Todo added")
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted")
    return redirect('/todo')


@app.route('/todo/<id>/completed', methods=['POST'])
@login_required
def todo_completed(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if todo.completed == 1:
        todo.mark_uncompleted()
        db.session.commit()
    else:
        todo.mark_completed()
        db.session.commit()
    return redirect('/todo')