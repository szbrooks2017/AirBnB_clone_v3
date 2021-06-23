#!/usr/bin/python3
""" creating resources"""
from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models import storage
import json
resource = storage.all(State)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ getting state resource"""
    obj = []
    for value in resource.values():
        obj.append(value.to_dict())
    return jsonify(obj)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """ getting state id"""
    for value in resource.values():
        if value.id == state_id:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """ deleting"""
    for value in resource.values():
        if value.id == state_id:
            storage.delete(value)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creating a new state resource"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data['name']:
        abort(400, 'Missing name')
    obj = State(**data)
    storage.new(obj)
    storage.save()
    obj = obj.to_dict()
    return jsonify(obj), 201


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updating a new state resource"""
    for value in resource.values():
        if value.id == state_id:
            obj = value
            break
    else:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')
    obj_dict = request.get_json()
    bad_list = ['id', 'created_at', 'updated_at']
    for key, value in obj_dict.items():
        if key not in bad_list:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
