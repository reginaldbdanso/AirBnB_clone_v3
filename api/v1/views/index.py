#!/usr/bin/python3
""" Index module """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """ Returns status """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats')
def stats():
    """ Retrieves the number of each objects by type """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
