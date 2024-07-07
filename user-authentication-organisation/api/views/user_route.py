#!/usr/bin/env python3
"""
Module supplies routes to user resources
"""
from . import db
from flask import Blueprint, request, jsonify
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/api/users/<id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def user_details(id):
    """
    returns the details of a user
    """
    if id != get_jwt_identity():
        return jsonify({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }), 401
    user = User.query.filter(User.userId == id).first()
    response = {
        "status": "success",
        "message": f"{user.firstName}'s records",
        "data": {
            "userId": user.userId,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phone": user.phone
            }
        }
    return jsonify(response)
