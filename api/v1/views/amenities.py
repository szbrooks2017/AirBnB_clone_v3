#!/usr/bin/python3
""" default API functions for amenities"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ getting amenity resource"""
    resource = storage.all(Amenity)
    obj = []
    for value in resource.values():
        obj.append(value.to_dict())
    return jsonify(obj)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_id(amenity_id):
    """ getting amenity id"""
    value = storage.get(Amenity, amenity_id)
    if value is None:
        abort(404)
    return jsonify(value.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ deleting an amenity"""
    value = storage.get(Amenity, amenity_id)
    if value is None:
        abort(404)
    storage.delete(value)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """creating a new amenity resource"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    obj = Amenity(**data)
    storage.new(obj)
    storage.save()
    obj = obj.to_dict()
    return jsonify(obj), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ updating a new amenity resource"""
    obj = storage.get(Amenity, amenity_id)
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
