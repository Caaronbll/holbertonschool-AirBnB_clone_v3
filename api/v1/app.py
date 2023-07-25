#!/usr/bin/python3
"""Creating an instance of Flask"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


# Creating flask app instance
app = Flask(__name__)


# Enable Cross-Origin Resource Sharing (CORS)
# to allow requests from any origin
CORS(app, origins="0.0.0.0")

# Register the app_views blueprint, contains API Rolutes
app.register_blueprint(app_views)

# Define teardown_appcontext decorator to close database
# Method that tears down app context
@app.teardown_appcontext
def teardown_appcontext(self):
    """Calls the close method in storage"""
    storage.close()


# 404 error
@app.errorhandler(404)
def not_found(error):
    """404 error"""
    return jsonify({"error": "Not found"}), 404

# If main file
if __name__ == '__main__':
    # Gets host and port from env variables
    hosts = getenv('HBNB_API_HOST', default='0.0.0.0')
    ports = getenv('HBNB_API_PORT', default=5000)

    # Runs the application
    app.run(host=hosts, port=ports, threaded=True)