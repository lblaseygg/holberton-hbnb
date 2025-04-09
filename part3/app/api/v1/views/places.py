from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.place import Place
from app.api.v1 import api_v1

@api_v1.route('/places', methods=['GET'])
def get_places():
    """Get all places (public endpoint)."""
    places = Place.query.all()
    return jsonify([place.to_dict() for place in places])

@api_v1.route('/places/<int:place_id>', methods=['GET'])
def get_place(place_id):
    """Get a specific place (public endpoint)."""
    place = Place.query.get_or_404(place_id)
    return jsonify(place.to_dict())

@api_v1.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    """Create a new place (authenticated endpoint)."""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new place
    place = Place(
        title=data['title'],
        description=data.get('description', ''),
        price=data['price'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        owner_id=current_user['id']
    )
    
    db.session.add(place)
    db.session.commit()
    
    return jsonify(place.to_dict()), 201

@api_v1.route('/places/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """Update a place (authenticated endpoint)."""
    current_user = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    
    # Check ownership or admin status
    if not current_user.get('is_admin', False) and place.owner_id != current_user['id']:
        return jsonify({'error': 'Unauthorized action'}), 403
    
    data = request.get_json()
    
    # Update place fields
    if 'title' in data:
        place.title = data['title']
    if 'description' in data:
        place.description = data['description']
    if 'price' in data:
        place.price = data['price']
    if 'latitude' in data:
        place.latitude = data['latitude']
    if 'longitude' in data:
        place.longitude = data['longitude']
    
    db.session.commit()
    return jsonify(place.to_dict())

@api_v1.route('/places/<int:place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    """Delete a place (authenticated endpoint)."""
    current_user = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    
    # Check ownership or admin status
    if not current_user.get('is_admin', False) and place.owner_id != current_user['id']:
        return jsonify({'error': 'Unauthorized action'}), 403
    
    db.session.delete(place)
    db.session.commit()
    return jsonify({'message': 'Place deleted successfully'}), 200 