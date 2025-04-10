from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Define the models for related entities
user_model = api.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the reviewer'),
    'last_name': fields.String(description='Last name of the reviewer'),
    'email': fields.String(description='Email of the reviewer')
})

place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place')
})

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Define the review response model
review_response = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user': fields.Nested(user_model, description='User who wrote the review'),
    'place': fields.Nested(place_model, description='Place being reviewed')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created', review_response)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or place not found')
    def post(self):
        """Register a new review"""
        review_data = api.payload

        new_review = facade.create_review(review_data)
        if not new_review:
            return {'error': 'Invalid input data or user/place not found'}, 400

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user': {
                'id': new_review.user.id,
                'first_name': new_review.user.first_name,
                'last_name': new_review.user.last_name,
                'email': new_review.user.email
            },
            'place': {
                'id': new_review.place.id,
                'title': new_review.place.title
            }
        }, 201

    @api.response(200, 'List of reviews retrieved successfully', [review_response])
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user': {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'email': review.user.email
            },
            'place': {
                'id': review.place.id,
                'title': review.place.title
            }
        } for review in reviews], 200

@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', review_response)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user': {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'email': review.user.email
            },
            'place': {
                'id': review.place.id,
                'title': review.place.title
            }
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review successfully updated', review_response)
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review information"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        review_data = api.payload
        updated_review = facade.update_review(review_id, review_data)
        if not updated_review:
            return {'error': 'Invalid input data'}, 400

        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user': {
                'id': updated_review.user.id,
                'first_name': updated_review.user.first_name,
                'last_name': updated_review.user.last_name,
                'email': updated_review.user.email
            },
            'place': {
                'id': updated_review.place.id,
                'title': updated_review.place.title
            }
        }, 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if not facade.delete_review(review_id):
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully', [review_response])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user': {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'email': review.user.email
            },
            'place': {
                'id': review.place.id,
                'title': review.place.title
            }
        } for review in reviews], 200 