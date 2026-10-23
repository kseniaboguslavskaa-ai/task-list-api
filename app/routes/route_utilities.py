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