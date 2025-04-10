from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the amenity response model
amenity_response = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created', amenity_response)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        new_amenity = facade.create_amenity(amenity_data)
        if not new_amenity:
            return {'error': 'Invalid input data'}, 400

        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully', [amenity_response])
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [{
            'id': amenity.id,
            'name': amenity.name
        } for amenity in amenities], 200

@api.route('/<amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', amenity_response)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated', amenity_response)
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update amenity information"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Invalid input data'}, 400

        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200 