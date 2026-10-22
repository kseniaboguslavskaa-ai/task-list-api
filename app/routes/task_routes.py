from flask import Blueprint, jsonify, request
from ..db import db
from ..models.task import Task
from .route_utilities import validate_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.get("")
def get_tasks():
    sort = request.args.get("sort")
    query = db.select(Task)

    if sort == "asc":
        query = query.order_by(Task.title.asc())
    elif sort == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query).all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200

@tasks_bp.post("")
def create_task():
    task_data = request.get_json()

    try:
        new_task = Task.from_dict(task_data)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201

@tasks_bp.get("/<task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify(task.to_dict()), 200

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    task_data = request.get_json()

    task.title = task_data["title"]
    task.description = task_data["description"]

    db.session.commit()

    return jsonify(None), 204

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify(None), 204