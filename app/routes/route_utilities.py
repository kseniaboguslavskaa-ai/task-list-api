from flask import abort, jsonify, make_response
from ..db import db

def validate_model(model, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response(jsonify({"details": "Invalid id"}), 400))

    instance = db.session.get(model, model_id)

    if instance is None:
        if model.__name__ == "Goal":
            abort(make_response(jsonify({"message": "Goal not found"}), 404))
        abort(make_response(jsonify({"details": "Not found"}), 404))

    return instance

def create_model(model, model_data):
    try:
        new_instance = model.from_dict(model_data)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.add(new_instance)
    db.session.commit()

    return new_instance.to_dict(), 201