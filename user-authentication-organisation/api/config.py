#!/usr/bin/env python3
"""
Contains configuration for the app
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Defines a Config object with necessary app configuration
    """
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """
    Defines Development config object
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Defines Testing configuration object
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URI')
    DEBUG = True


class ProductionConfig(Config):
    """
    Define Production configuration object
    """
    DEBUG = False
