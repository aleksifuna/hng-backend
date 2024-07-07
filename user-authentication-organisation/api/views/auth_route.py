#!/usr/bin/env python3
"""
Module supplies routes to authentication resources
"""
from . import db
from flask import Blueprint, request, jsonify
from models.user import User
from models.organisation import Organisation
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/auth/register', methods=['POST'], strict_slashes=False)
def register_user():
    """
    Registers user and creates a login token
    """
    error_response = {
        'errors': []
    }
    data = request.json
    if not data:
        return jsonify({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
            }), 400
    required = ['firstName', 'lastName', 'email', 'password']
    for field in required:
        if field not in data:
            error_response['errors'].append({
                "field": field,
                "message": f"{field} Missing"
            })
    first_name = data.get('firstName')
    if first_name and not isinstance(first_name, str):
        error_response['errors'].append({
            "field": "firstName",
            "message": "firstName should be a string"
            })
    last_name = data.get('lastName')
    if last_name and not isinstance(last_name, str):
        error_response['errors'].append({
            "field": "lastName",
            "message": "lastName should be a string"
        })
    email = data.get('email')
    if email and not isinstance(email, str):
        error_response['errors'].append({
            "field": "email",
            "message": "email should be a string"
        })
    password = data.get('password')
    if password and not isinstance(password, str):
        error_response['errors'].append({
            "field": "password",
            "message": "password should be a string"
        })
    phone = data.get('phone')
    if phone and not isinstance(phone, str):
        error_response['errors'].append({
            "field": "phone",
            "message": "phone should be a string"
        })
    if len(error_response["errors"]) != 0:
        return jsonify(error_response), 422
    user = User.query.filter(User.email == email).first()
    if user:
        return jsonify({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
            }), 400
    user = User()
    setattr(user, 'firstName', first_name)
    setattr(user, 'lastName', last_name)
    setattr(user, 'email', email)
    if phone:
        setattr(user, 'phone', phone)
    user.set_password(password)
    db.session.add(user)

    org = Organisation()
    setattr(org, "name", f"{first_name}'s Organisation")
    db.session.add(org)
    org.users.append(user)
    db.session.commit()
    access_token = create_access_token(identity=user.userId)
    response = {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": {
                "userId": user.userId,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
                "phone": user.phone
            }
        }
    }
    return jsonify(response), 201


@auth_bp.route('/auth/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles login route
    """
    data = request.json
    if not data:
        return jsonify({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
            }), 401
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
            }), 401
    user = User.query.filter(User.email == email).first()
    if not user:
        return jsonify({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
            }), 401
    if not user.check_password(password):
        return jsonify({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
            }), 401
    access_token = create_access_token(identity=user.userId)
    response = {
        "status": "success",
        "message": "Login successful",
        "data": {
            "accessToken": access_token,
            "user": {
                "userId": user.userId,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
                "phone": user.phone
            }
        }
    }
    return jsonify(response), 200
