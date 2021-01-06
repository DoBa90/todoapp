from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dominiquebataille@localhost:5432/todoapp'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=True, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, description: {self.description}, complete: {self.complete}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todo = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList ID: {self.id}, name: {self.name}, todos: {self.todos}>'

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    list_id = request.get_json()['list_id']
    todoInput = Todo(description=description, complete=False, list_id=list_id)
    db.session.add(todoInput)
    db.session.commit()
    body['id'] = todoInput.id
    body['completed'] = todoInput.completed
    body['description'] = todoInput.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todocheck = Todo.query.get(todo_id)
        todocheck.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>/delete-item', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todoItem = Todo.query.get(todo_id)
        db.session.delete(todoItem)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

@app.route('/lists/<list_id>')
def get_lists_todo(list_id):
    return render_template('index.html', 
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all(),
    active_list=TodoList.query.get(list_id),
    list_todos=TodoList.query.all())

@app.route('/')
def index():
  return redirect(url_for('get_lists_todo', list_id=1))