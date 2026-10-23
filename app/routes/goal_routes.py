from flask import Blueprint, jsonify, request
from ..db import db
from ..models.goal import Goal
from .route_utilities import validate_model
from ..models.task import Task

goals_bp = Blueprint(
    "goals_bp",
    __name__,
    url_prefix="/goals"
)

@goals_bp.errorhandler(404)
def goal_not_found(error):
    return jsonify({"message":"Goal not found"}), 404

@goals_bp.post("")
def create_goal():
    goal_data = request.get_json()

    try:
        new_goal = Goal.from_dict(goal_data)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_dict()), 201

@goals_bp.get("")
def get_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query).all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200

@goals_bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify(goal.to_dict()), 200

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_data = request.get_json()

    try:
        goal.title = goal_data["title"]
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.commit()

    return jsonify(None), 204

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify(None), 204

@goals_bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    if not isinstance(request_body, dict):
        return jsonify({"details": "Invalid data"}), 400
    task_ids = request_body.get("task_ids")

    if not isinstance(task_ids, list):
        return jsonify({"details": "Invalid data"}), 400

    tasks = []

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        tasks.append(task)

    goal.tasks = tasks
    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }), 200

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    goal_response = goal.to_dict()
    goal_response["tasks"] = tasks_response

    return jsonify(goal_response), 200