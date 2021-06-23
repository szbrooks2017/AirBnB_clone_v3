#!/usr/bin/python3
""" default API functions for places"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ getting place resource"""
    cities = storage.all(City)
    if "City." + str(city_id) not in cities:
        abort(404)
    resource = storage.all(Place)
    obj = []
    for value in resource.values():
        if value.city_id == city_id:
            obj.append(value.to_dict())
    return jsonify(obj)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """ getting place id"""
    value = storage.get(Place, place_id)
    if value is None:
        abort(404)
    return jsonify(value.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ deleting a place"""
    value = storage.get(Place, place_id)
    if value is None:
        abort(404)
    storage.delete(value)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """creating a new place resource"""
    if storage.get(City, city_id) is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    data['city_id'] = city_id
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    obj = Place(**data)
    storage.new(obj)
    storage.save()
    obj = obj.to_dict()
    return jsonify(obj), 201


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updating a new place resource"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    obj_dict = request.get_json()
    bad_list = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for key, value in obj_dict.items():
        if key not in bad_list:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
