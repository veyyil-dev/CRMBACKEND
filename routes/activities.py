import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db
from models.activity import Activity

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/activities', methods=['GET'])
def get_activities():
    contact_id = request.args.get('contact_id')
    
    query = Activity.query
    
    if contact_id:
        query = query.filter_by(contact_id=contact_id)
    
    activities = query.order_by(Activity.date.desc()).all()
    return jsonify([activity.to_dict() for activity in activities])

@activities_bp.route('/activities/<activity_id>', methods=['GET'])
def get_activity(activity_id):
    activity = Activity.query.get(activity_id)
    
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    return jsonify(activity.to_dict())

@activities_bp.route('/activities', methods=['POST'])
def create_activity():
    data = request.json
    
    # Validate required fields
    required_fields = ['contact_id', 'type', 'notes', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # Parse date string to datetime object
        date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
        
        # Create new activity
        activity = Activity(
            id=str(uuid.uuid4()),
            contact_id=data['contact_id'],
            type=data['type'],
            notes=data['notes'],
            date=date
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify(activity.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/activities/<activity_id>', methods=['PUT'])
def update_activity(activity_id):
    activity = Activity.query.get(activity_id)
    
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    data = request.json
    
    try:
        if 'type' in data:
            activity.type = data['type']
        
        if 'notes' in data:
            activity.notes = data['notes']
        
        if 'date' in data:
            activity.date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
        
        db.session.commit()
        
        return jsonify(activity.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/activities/<activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    activity = Activity.query.get(activity_id)
    
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    try:
        db.session.delete(activity)
        db.session.commit()
        
        return jsonify({'message': 'Activity deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 