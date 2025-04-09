from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig

# Initialize extensions
bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    """
    Application Factory pattern for creating Flask application instances.
    
    Args:
        config_class: Configuration class to use for the application.
                     Defaults to DevelopmentConfig.
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask application instance
    app = Flask(__name__)
    
    # Load configuration from the provided config class
    app.config.from_object(config_class)
    
    # Initialize extensions
    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    return app 