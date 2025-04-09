from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.amenity import Amenity
from app.api.v1 import api_v1
from app.utils.decorators import admin_required

@api_v1.route('/amenities', methods=['GET'])
def get_amenities():
    """Get all amenities (public endpoint)."""
    amenities = Amenity.query.all()
    return jsonify([amenity.to_dict() for amenity in amenities])

@api_v1.route('/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Get a specific amenity (public endpoint)."""
    amenity = Amenity.query.get_or_404(amenity_id)
    return jsonify(amenity.to_dict())

@api_v1.route('/amenities', methods=['POST'])
@jwt_required()
@admin_required
def create_amenity():
    """Create a new amenity (admin only)."""
    data = request.get_json()
    
    # Validate required fields
    if 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400
    
    # Check if amenity already exists
    if Amenity.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Amenity already exists'}), 400
    
    # Create new amenity
    amenity = Amenity(
        name=data['name'],
        description=data.get('description')
    )
    
    db.session.add(amenity)
    db.session.commit()
    
    return jsonify(amenity.to_dict()), 201

@api_v1.route('/amenities/<int:amenity_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_amenity(amenity_id):
    """Update an amenity (admin only)."""
    amenity = Amenity.query.get_or_404(amenity_id)
    data = request.get_json()
    
    # Update amenity fields
    if 'name' in data:
        # Check if new name is already in use
        existing_amenity = Amenity.query.filter_by(name=data['name']).first()
        if existing_amenity and existing_amenity.id != amenity_id:
            return jsonify({'error': 'Amenity name already exists'}), 400
        amenity.name = data['name']
    
    if 'description' in data:
        amenity.description = data['description']
    
    db.session.commit()
    return jsonify(amenity.to_dict())

@api_v1.route('/amenities/<int:amenity_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_amenity(amenity_id):
    """Delete an amenity (admin only)."""
    amenity = Amenity.query.get_or_404(amenity_id)
    
    db.session.delete(amenity)
    db.session.commit()
    return jsonify({'message': 'Amenity deleted successfully'}), 200 