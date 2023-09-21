import sqlite3
import datetime
import enum

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Engine, event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
db = SQLAlchemy(app)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class BoardStatusEnum(enum.Enum):
    OPEN = 'OPEN'
    ARCHIVED = 'ARCHIVED'


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    status = db.Column(db.String(8), default=BoardStatusEnum.OPEN.value, nullable=False)
    tasks = db.relationship('Task', backref='board', cascade='delete', passive_deletes=True)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status,
            'tasks': [task.id for task in self.tasks]
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    status = db.Column(db.Boolean, default=False)
    text = db.Column(db.String(255))
    board_id = db.Column(db.Integer, db.ForeignKey('board.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {'id': self.id,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'status': self.status,
                'text': self.text,
                'board_id': self.board_id
                }


@app.route('/boards', methods=['GET'])
def get_boards():
    boards = Board.query.all()
    return jsonify({'boards': [board.to_dict() for board in boards]})


@app.route('/boards', methods=['POST'])
def create_board():
    board = Board()
    db.session.add(board)
    db.session.commit()
    return jsonify(board.to_dict())


@app.route('/tasks', methods=['GET'])
def get_tasks():
    params = request.args
    status = params.get('status')
    if status is not None:
        if status.lower() == 'true':
            status = True
        elif status.lower() == 'false':
            status = False
        else:
            status = None
    board_id = int(params.get('board_id', 0))

    query = Task.query
    if status is not None:
        query = query.filter(Task.status == status)
    if board_id:
        query = query.filter(Task.board_id == board_id)
    tasks = query.all()
    return jsonify({'tasks': [task.to_dict() for task in tasks]})


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict())


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()[0]
    task = Task(
        status=data['status'],
        text=data['text'],
        board_id=data['board_id']
    )
    try:
        db.session.add(task)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create tasks - {str(e)}'}), 500
    return jsonify(task.to_dict())


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()[0]
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    task.status = data.get('status', task.status)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update task - {str(e)}'}), 500
    return jsonify(task.to_dict())


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({}), 204


if __name__ == '__main__':
    app.run(debug=True)
