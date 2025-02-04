from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.title}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    new_todo = Todo(title=title, description=description)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

# Mark a Todo as Completed
@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = True
        db.session.commit()
    return redirect(url_for('index'))

# Edit an Existing Todo
@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

# Delete a Todo
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
