from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import DevelopmentConfig
import logging

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
    
    Raises:
        ImportError: If the configuration class cannot be imported
        AttributeError: If the configuration class is missing required attributes
    """
    # Create Flask application instance
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration from the provided config class
        app.config.from_object(config_class)
        logger.info(f"Successfully loaded configuration from {config_class.__name__}")
        
        # Log important configuration values (excluding sensitive ones)
        logger.debug(f"Environment: {app.config.get('ENV', 'not set')}")
        logger.debug(f"Debug mode: {app.config.get('DEBUG', 'not set')}")
        logger.debug(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'not set')}")
        
    except ImportError as e:
        logger.error(f"Failed to import configuration class: {e}")
        raise
    except AttributeError as e:
        logger.error(f"Configuration class missing required attributes: {e}")
        raise
    
    # Initialize extensions
    try:
        bcrypt.init_app(app)
        db.init_app(app)
        jwt.init_app(app)
        logger.info("Successfully initialized all extensions")
    except Exception as e:
        logger.error(f"Failed to initialize extensions: {e}")
        raise
    
    # Enable CORS with more permissive settings
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:*", "http://localhost:*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    try:
        from app.api.v1 import api_v1
        app.register_blueprint(api_v1, url_prefix='/api/v1')
        logger.info("Successfully registered API v1 blueprint")
    except Exception as e:
        logger.error(f"Failed to register blueprints: {e}")
        raise
    
    # Log registered routes
    logger.debug("Registered routes:")
    for rule in app.url_map.iter_rules():
        logger.debug(f"{rule.endpoint}: {rule.methods} {rule}")
    
    return app 