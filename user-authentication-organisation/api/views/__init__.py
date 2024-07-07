#!/usr/bin/env/ python3
"""
Webapp factory
"""
from api.config import DevelopmentConfig, TestingConfig, ProductionConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os

load_dotenv()

db = SQLAlchemy()


def create_app(environment: str):
    """
    Create the flask app
    """
    app = Flask(__name__)
    if environment == 'dev':
        app.config.from_object(DevelopmentConfig)
    elif environment == 'test':
        app.config.from_object(TestingConfig)
    elif environment == 'production':
        app.config.from_object(ProductionConfig)
    CORS(app, supports_credentials=True, resources={'/*': {'origins': '*'}})
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    with app.app_context():
        from .user_route import user_bp
        from .auth_route import auth_bp
        from .org_route import org_bp

        app.register_blueprint(user_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(org_bp)

        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
    return app
