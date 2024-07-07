#!/usr/bin/env python3
"""
Module supplies routes to organisation resources
"""
from . import db
from flask import Blueprint, request, jsonify
from models.user import User
from models.organisation import Organisation
from flask_jwt_extended import jwt_required, get_jwt_identity

org_bp = Blueprint('org_bp', __name__)


@org_bp.route('/api/organisations', methods=['GET'], strict_slashes=False)
@jwt_required()
def organisations_details():
    """
    returns organisations that a user belongs to or created
    """
    id = get_jwt_identity()
    user = User.query.filter(User.userId == id).first()
    orgs = []
    for org in user.organisations:
        orgs.append({
            "orgId": org.orgId,
            "name": org.name,
            "description": org.description
        })
    response = {
        "status": "success",
        "message": f"{user.firstName}'s Organisations",
        "data": {
            "organisations": orgs
            }
        }
    return jsonify(response), 200


@org_bp.route(
        '/api/organisations/<orgId>',
        methods=['GET'],
        strict_slashes=False
        )
@jwt_required()
def get_orgs(orgId):
    """
    Returns the details of a specific organisation
    """
    org = Organisation.query.filter(Organisation.orgId == orgId).first()
    if not org:
        return jsonify({
            "status": "Bad Request",
            "message": "Organisation Not Found",
            "statusCode": 400
            }), 400
    response = {
        "status": "success",
        "message": f"{org.name}'s details",
        "data": {
            "orgId": org.orgId,
            "name": org.name,
            "description": org.description
            }
        }
    return jsonify(response), 200


@org_bp.route('/api/organisations', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_organisation():
    """
    Registers a new organisation
    """
    data = request.json
    if not data:
        return jsonify({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
            }), 400
    name = data.get('name')
    description = data.get('description')
    if not name or not isinstance(name, str):
        return jsonify({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
            }), 400
    if description and not isinstance(description, str):
        return jsonify({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
            }), 400
    org = Organisation()
    setattr(org, 'name', name)
    if description:
        setattr(org, 'description', description)
    db.session.add(org)
    db.session.commit()
    response = {
        "status": "success",
        "message": "Organisation created successfully",
        "data": {
            "orgId": org.orgId,
            "name": org.name,
            "description": org.description
            }
        }
    return jsonify(response), 201


@org_bp.route(
        '/api/organisations/<orgId>/users',
        methods=['POST'],
        strict_slashes=False
        )
def add_user(orgId):
    """
    Adds a users to an organisation
    """
    data = request.json
    if not data:
        return jsonify({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
            }), 400
    userId = data.get('userId')
    if not userId:
        return jsonify({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
            }), 400
    org = Organisation.query.filter(Organisation.orgId == orgId).first()
    if not org:
        return jsonify({
            "status": "Bad Request",
            "message": "Organisation Not Found",
            "statusCode": 400
            }), 400
    user = User.query.filter(User.userId == userId).first()
    if not user:
        return jsonify({
            "status": "Bad Request",
            "message": "User Not Found",
            "statusCode": 400
            }), 400
    org.users.append(user)
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "User added to organisation successfully"
        }), 200
