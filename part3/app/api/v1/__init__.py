from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)

from app.api.v1.views import users, auth, places, reviews, amenities  # noqa 