#!/usr/bin/python3
""" creating resources"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models.state import State
from models import storage
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ getting state resource"""
    resource = storage.all(State)
    obj = []
    for value in resource.values():
        obj.append(value.to_dict())
    return jsonify(obj)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """ getting state id"""
    value = storage.get(State, state_id)
    if value is None:
        abort(404)
    return jsonify(value.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deleting"""
    value = storage.get(State, state_id)
    if value is None:
        abort(404)
    storage.delete(value)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creating a new state resource"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    obj = State(**data)
    storage.new(obj)
    storage.save()
    obj = obj.to_dict()
    return jsonify(obj), 201


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updating a new state resource"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    obj_dict = request.get_json()
    bad_list = ['id', 'created_at', 'updated_at']
    for key, value in obj_dict.items():
        if key not in bad_list:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
