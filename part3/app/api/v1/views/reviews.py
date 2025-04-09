from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.review import Review
from app.models.place import Place
from app.api.v1 import api_v1

@api_v1.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    """Create a new review (authenticated endpoint)."""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['place_id', 'text', 'rating']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Get the place
    place = Place.query.get_or_404(data['place_id'])
    
    # Check if user is the owner of the place (unless admin)
    if not current_user.get('is_admin', False) and place.owner_id == current_user['id']:
        return jsonify({'error': 'You cannot review your own place'}), 400
    
    # Check if user has already reviewed this place (unless admin)
    if not current_user.get('is_admin', False):
        existing_review = Review.query.filter_by(
            user_id=current_user['id'],
            place_id=data['place_id']
        ).first()
        
        if existing_review:
            return jsonify({'error': 'You have already reviewed this place'}), 400
    
    # Create new review
    review = Review(
        text=data['text'],
        rating=data['rating'],
        user_id=current_user['id'],
        place_id=data['place_id']
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify(review.to_dict()), 201

@api_v1.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update a review (authenticated endpoint)."""
    current_user = get_jwt_identity()
    review = Review.query.get_or_404(review_id)
    
    # Check ownership or admin status
    if not current_user.get('is_admin', False) and review.user_id != current_user['id']:
        return jsonify({'error': 'Unauthorized action'}), 403
    
    data = request.get_json()
    
    # Update review fields
    if 'text' in data:
        review.text = data['text']
    if 'rating' in data:
        review.rating = data['rating']
    
    db.session.commit()
    return jsonify(review.to_dict())

@api_v1.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review (authenticated endpoint)."""
    current_user = get_jwt_identity()
    review = Review.query.get_or_404(review_id)
    
    # Check ownership or admin status
    if not current_user.get('is_admin', False) and review.user_id != current_user['id']:
        return jsonify({'error': 'Unauthorized action'}), 403
    
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'}), 200 