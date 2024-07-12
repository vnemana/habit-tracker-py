from flask import Blueprint, request, jsonify, abort
from ..db import db
from ..models import Habit

habit_bp = Blueprint('habit_bp', __name__)

@habit_bp.route('/habits', methods=['POST'])
def create_habit():
    data = request.get_json()
    new_habit = Habit(
        user_id=data['user_id'],
        name=data['name'],
        frequency=data['frequency'],
        time_of_day=data['time_of_day']
    )
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({'id': new_habit.id, 'name': new_habit.name}), 201

@habit_bp.route('/habits', methods=['GET'])
def get_habits():
    habits = db.session.query(Habit).all()
    return jsonify([
        {'id': habit.id, 'user_id': habit.user_id, 'name': habit.name, 'frequency': habit.frequency, 'time_of_day': habit.time_of_day}
        for habit in habits
    ]), 200

@habit_bp.route('/habits/<int:id>', methods=['GET'])
def get_habit(id):
    habit = db.session.get(Habit, id)
    if habit is None:
        abort(404)
    return jsonify({
        'id': habit.id, 'user_id': habit.user_id, 'name': habit.name, 'frequency': habit.frequency, 'time_of_day': habit.time_of_day
    }), 200

@habit_bp.route('/habits/<int:id>', methods=['PUT'])
def update_habit(id):
    data = request.get_json()
    habit = db.session.get(Habit, id)
    if habit is None:
        abort(404)
    habit.user_id = data.get('user_id', habit.user_id)
    habit.name = data.get('name', habit.name)
    habit.frequency = data.get('frequency', habit.frequency)
    habit.time_of_day = data.get('time_of_day', habit.time_of_day)
    db.session.commit()
    return jsonify({
        'id': habit.id, 'user_id': habit.user_id, 'name': habit.name, 'frequency': habit.frequency, 'time_of_day': habit.time_of_day
    }), 200

@habit_bp.route('/habits/<int:id>', methods=['DELETE'])
def delete_habit(id):
    habit = db.session.get(Habit, id)
    if habit is None:
        abort(404)
    db.session.delete(habit)
    db.session.commit()
    return jsonify({'message': 'Habit deleted'}), 200
