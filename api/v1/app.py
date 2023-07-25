#!/usr/bin/python3
"""Returns the status of the API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

# Create a Flask app instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
# to allow requests from any origin
CORS(app, origins="0.0.0.0")

# Register the app_views blueprint, which contains the API routes
app.register_blueprint(app_views)


# Define a teardown_appcontext decorator to close the database
# session after each request
@app.teardown_appcontext
def teardown_appcontext(self):
    """Exits storage by calling close"""
    storage.close()


# Define an errorhandler for 404 errors to handle resource not found
@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404

# Start the Flask application
if __name__ == "__main__":
    # Get the host and port from environment variables, or use default values
    hosts = getenv('HBNB_API_HOST', default='0.0.0.0')
    ports = getenv('HBNB_API_PORT', default=5000)

    # Run the Flask app on the specified host and port, with threading enabled
    app.run(host=hosts, port=ports, threaded=True)
