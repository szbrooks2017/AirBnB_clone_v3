#!/usr/bin/python3
""" default API functions for users"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ getting user resource"""
    resource = storage.all(User)
    obj = []
    for value in resource.values():
        obj.append(value.to_dict())
    return jsonify(obj)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """ getting user id"""
    value = storage.get(User, user_id)
    if value is None:
        abort(404)
    return jsonify(value.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ deleting a user"""
    value = storage.get(User, user_id)
    if value is None:
        abort(404)
    storage.delete(value)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """creating a new user resource"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    obj = User(**data)
    storage.new(obj)
    storage.save()
    obj = obj.to_dict()
    return jsonify(obj), 201


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updating a new user resource"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    obj_dict = request.get_json()
    bad_list = ['id', 'created_at', 'updated_at', 'email']
    for key, value in obj_dict.items():
        if key not in bad_list:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
