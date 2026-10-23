from flask import Blueprint, jsonify, request
from ..db import db
from ..models.goal import Goal
from .route_utilities import validate_model

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