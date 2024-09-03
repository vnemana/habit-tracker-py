from flask import Blueprint, request, jsonify, abort
from ..db import db
from ..models import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    auth_provider = data.get('auth_provider')
    provider_id = data.get('provider_id')
    name = data.get('name')
    email = data.get('email')

    # Check if user already exists
    existing_user = User.query.filter_by(auth_provider = auth_provider, provider_id = provider_id).first()
    if existing_user:
        return jsonify({'message': 'User already exists.'}), 400
    
    new_user = User(auth_provider = auth_provider, provider_id = provider_id, name = name, email = email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users]), 200

@user_bp.route('/users/<string:id>', methods=['GET'])
def get_user(id):
    data = request.json
    user = User.query.filter_by(auth_provider = data.get('auth_provider'), provider_id = id).first()
    if user is None:
        abort(404)
    return jsonify({'id': user.id, 'name': user.name}), 200

@user_bp.route('/users/<string:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.filter_by(auth_provider = data.get('auth_provider'), provider_id = id).first()
    if user is None:
        abort(404)
    user.name = data.get('name')
    user.email = data.get('email')
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name}), 200

@user_bp.route('/users/<string:id>', methods=['DELETE'])
def delete_user(id):
    data = request.get_json()
    user = User.query.filter_by(auth_provider = data.get('auth_provider'), provider_id = id).first()
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
