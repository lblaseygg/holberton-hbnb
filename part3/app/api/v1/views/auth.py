from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.api.v1 import api_v1

@api_v1.route('/auth/login', methods=['POST'])
def login():
    """Authenticate user and return a JWT token."""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    # Get user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if user exists and password is correct
    if not user or not user.verify_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Create access token
    access_token = create_access_token(
        identity={
            'id': user.id,
            'is_admin': user.is_admin
        }
    )
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@api_v1.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information."""
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

@api_v1.route('/auth/protected', methods=['GET'])
@jwt_required()
def protected():
    """A protected endpoint that requires a valid JWT token."""
    current_user = get_jwt_identity()
    return jsonify({
        'message': f'Hello, user {current_user["id"]}',
        'is_admin': current_user['is_admin']
    }), 200 