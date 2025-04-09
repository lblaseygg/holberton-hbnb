from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.api.v1 import api_v1
from app.utils.decorators import admin_required

@api_v1.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    """Create a new user (admin only)."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        is_admin=data.get('is_admin', False)
    )
    
    # Add user to database
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201

@api_v1.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details by ID."""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@api_v1.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user information."""
    current_user = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Check if user is admin or trying to modify their own data
    if not current_user.get('is_admin', False) and current_user['id'] != user_id:
        return jsonify({'error': 'Unauthorized action'}), 403
    
    data = request.get_json()
    
    # Only admins can modify email and password
    if not current_user.get('is_admin', False):
        if 'email' in data or 'password' in data:
            return jsonify({'error': 'You cannot modify email or password'}), 400
    
    # Update user fields
    if 'email' in data:
        # Check if email is already in use
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Email already in use'}), 400
        user.email = data['email']
    
    if 'password' in data:
        user.hash_password(data['password'])
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'is_admin' in data and current_user.get('is_admin', False):
        user.is_admin = data['is_admin']
    
    db.session.commit()
    return jsonify(user.to_dict()) 