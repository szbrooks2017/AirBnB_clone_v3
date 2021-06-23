#!/usr/bin/python3
""" module for city API functions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ getting all cities in given state"""
    states = storage.all(State)
    if "State." + str(state_id) not in states:
        abort(404)
    resource = storage.all(City)
    objl = []
    for value in resource.values():
        if value.state_id == state_id:
            objl.append(value.to_dict())
    return jsonify(objl)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """ getting city id"""
    value = storage.get(City, city_id)
    if value is None:
        abort(404)
    return jsonify(value.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ deleting city"""
    value = storage.get(City, city_id)
    if value is None:
        abort(404)
    storage.delete(value)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """creating a new city in given state"""
    if storage.get(State, state_id) is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    data['state_id'] = state_id
    if "name" not in data:
        abort(400, description="Missing name")
    obj = City(**data)
    storage.new(obj)
    storage.save()
    obj = obj.to_dict()
    return jsonify(obj), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updating a new city resource"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    obj_dict = request.get_json()
    bad_list = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in obj_dict.items():
        if key not in bad_list:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
