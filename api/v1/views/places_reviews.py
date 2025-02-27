#!/usr/bin/python3
"""View for review objects: handles default RESTful API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


# Route to get all reviews of a specific place based on place_id
@app_views.route(
    "/places/<place_id>/reviews", methods=['GET'], strict_slashes=False)
def reviews(place_id):
    """Method retrieves list of all Review objects in a given Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)


# Route to get a single review based on review_id
@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Method retrieves a Review object in JSON format"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


# Route to delete a single review based on review_id
@app_views.route(
    "/reviews/<review_id>", methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """Method deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


# Route to create a new review under a specific place based on place_id
@app_views.route(
    "/places/<place_id>/reviews", methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Method creates a new Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    elif 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    elif 'text' not in request.json:
        abort(400, 'Missing text')
    review = request.get_json()
    review['place_id'] = place_id
    new_review = Review(**review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


# Route to update a single review based on review_id
@app_views.route(
    "/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Method updates an existing Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    elif not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    else:
        # List of attributes to ignore for updating (immutable attributes)
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())
