from app import app, db
from app.models import Task
from app.schemas import TaskSchema, UpdateTaskSchema
from flask import jsonify
from flask_apispec import marshal_with, use_kwargs
from sqlalchemy import exc


@app.route('/api/tasks', methods=['GET'])
def show_tasks():
    tasks = Task.query.all()
    if not tasks:
        return {'message': 'There are not any tasks!!'}
    schema = TaskSchema(many=True)
    return jsonify(schema.dump(tasks))


@app.route('/api/tasks', methods=['POST'])
@use_kwargs(TaskSchema)  # декоратор для десериализации входящих параметров, аналог schema.load (flask=apispec)
@marshal_with(TaskSchema)  # декоратор для сериализации данных,  один json объект
def add_task(**kwargs):
    task = Task(**kwargs)
    try:
        db.session.add(task)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'errors': str(e.args)})

    return task


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@marshal_with(TaskSchema)
def show_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({'message': f'No task with id = {task_id}'})

    return task


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@use_kwargs(UpdateTaskSchema)
@marshal_with(TaskSchema)
def update_task(task_id, **kwargs):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({'message': f'No task with id = {task_id}'})
    try:
        for key, value in kwargs.items():
            setattr(task, key, value)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'errors': str(e.args)})

    return task


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({'message': f'No task with id = {task_id}'})
    try:
        db.session.delete(task)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'errors': str(e.args)})

    return jsonify({'message': f'Task with id = {task_id} deleted'})


@app.errorhandler(422)  # обработка исключений схем marshmallow (422)
# при валидации, при отсутствующих полях в данных запроса, при неправильном формате даты
def handle_error(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


@app.errorhandler(404)
def handle_404(err):

    return jsonify({'message': 'This page not found!!'}), 400


@app.errorhandler(400)
def handle_400(err):

    return jsonify({'message': 'This request is bad. Please, try again!!'}), 400
