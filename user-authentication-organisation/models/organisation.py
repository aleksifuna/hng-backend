#!/usr/bin/env python3
"""
Organisation model
"""
from api.views import db
import bcrypt
from uuid import uuid4


class Organisation(db.Model):
    """
    Defines a User object's attributes and properties
    """
    __tablename__ = 'organisations'
    orgId = db.Column(db.String(), primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    def __init__(self):
        """
        Class constructor
        """
        self.orgId = str(uuid4())
