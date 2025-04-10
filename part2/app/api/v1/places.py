from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the review model for place
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user': fields.Nested(user_model, description='User who wrote the review')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

# Define the place response model
place_response = api.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created', place_response)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        new_place = facade.create_place(place_data)
        if not new_place:
            return {'error': 'Invalid input data or owner not found'}, 400

        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner': {
                'id': new_place.owner.id,
                'first_name': new_place.owner.first_name,
                'last_name': new_place.owner.last_name,
                'email': new_place.owner.email
            },
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in new_place.amenities],
            'reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name,
                    'email': review.user.email
                }
            } for review in new_place.reviews]
        }, 201

    @api.response(200, 'List of places retrieved successfully', [place_response])
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities],
            'reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name,
                    'email': review.user.email
                }
            } for review in place.reviews]
        } for place in places], 200

@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', place_response)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities],
            'reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name,
                    'email': review.user.email
                }
            } for review in place.reviews]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place successfully updated', place_response)
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place information"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            return {'error': 'Invalid input data'}, 400

        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner': {
                'id': updated_place.owner.id,
                'first_name': updated_place.owner.first_name,
                'last_name': updated_place.owner.last_name,
                'email': updated_place.owner.email
            },
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in updated_place.amenities],
            'reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name,
                    'email': review.user.email
                }
            } for review in updated_place.reviews]
        }, 200 