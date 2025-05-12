"""The app module, containing the app factory function."""
from flask import Flask
from flask_cors import CORS

from app.extensions import db, migrate, jwt
from app.routes import auth

def create_app(config_object="app.config"):
    # Create application factory. Param config_object, the configuration object to use.
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_blueprints(app)
    register_extensions(app)
    set_CORS(app)
    return app

def register_extensions(app):
    # Initialize the extensions.
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

def register_blueprints(app):
    # Register Flask blueprints.
    app.register_blueprint(auth.auth_bp)

def set_CORS(app):
    # Set CORS allowed domains
    CORS(app, origins=['*'])
    
