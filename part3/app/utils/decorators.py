from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def admin_required(fn):
    """Decorator to require admin privileges."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403
        return fn(*args, **kwargs)
    return wrapper 