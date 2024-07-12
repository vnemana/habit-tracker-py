from flask import Blueprint, request, jsonify, abort
from ..db import db
from ..models import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200

@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    if user is None:
        abort(404)
    return jsonify({'id': user.id, 'username': user.username}), 200

@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = db.session.get(User, id)
    if user is None:
        abort(404)
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 200

@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
