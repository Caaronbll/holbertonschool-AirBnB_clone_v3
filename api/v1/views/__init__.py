#!/usr/bin/python3
"""Importing Blueprint"""

from flask import Blueprint

# Creates an instance Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views for each endpoint (index, states, cities,
# amenities, places, users, places_reviews)
# This allows organizing the views in separate files
#  for better readability and maintainability.
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.places import *
from api.v1.views.users import *
from api.v1.views.places_reviews import *