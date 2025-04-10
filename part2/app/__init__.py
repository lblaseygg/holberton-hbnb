from flask import Flask
from flask_restx import Api
from app.api.v1.places import api as places_api
from app.api.v1.reviews import api as reviews_api
from app.api.v1.users import api as users_api

def create_app():
    app = Flask(__name__)
    api = Api(app, 
              version='1.0', 
              title='HBnB API',
              description='HBnB API Documentation',
              doc='/api/v1/')

    # Register API namespaces
    api.add_namespace(users_api, path='/api/v1/users')
    api.add_namespace(places_api, path='/api/v1/places')
    api.add_namespace(reviews_api, path='/api/v1/reviews')

    return app 