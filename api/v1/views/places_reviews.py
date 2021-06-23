#!/usr/bin/python3
""" default API functions for reviews"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ getting review resource"""
    places = storage.all(Place)
    if "Place." + str(place_id) not in places:
        abort(404)
    resource = storage.all(Review)
    obj = []
    for value in resource.values():
        if value.place_id == place_id:
            obj.append(value.to_dict())
    return jsonify(obj)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """ getting review id"""
    value = storage.get(Review, review_id)
    if value is None:
        abort(404)
    return jsonify(value.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deleting a review"""
    value = storage.get(Review, review_id)
    if value is None:
        abort(404)
    storage.delete(value)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """creating a new review resource"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    data['place_id'] = place_id
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if "text" not in data:
        abort(400, description="Missing text")
    obj = Review(**data)
    storage.new(obj)
    storage.save()
    obj = obj.to_dict()
    return jsonify(obj), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updating a new review resource"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    obj_dict = request.get_json()
    bad_list = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in obj_dict.items():
        if key not in bad_list:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
