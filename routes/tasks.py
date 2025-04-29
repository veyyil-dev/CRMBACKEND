import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db
from models.task import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    contact_id = request.args.get('contact_id')
    status = request.args.get('status')
    assigned_to = request.args.get('assigned_to')
    
    query = Task.query
    
    if contact_id:
        query = query.filter_by(contact_id=contact_id)
    
    if status:
        query = query.filter_by(status=status)
        
    if assigned_to:
        query = query.filter_by(assigned_to=assigned_to)
    
    tasks = query.order_by(Task.due_date.asc() if Task.due_date else Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task.to_dict())

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    
    # Validate required fields
    required_fields = ['title', 'contact_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # Parse due date if provided
        due_date = None
        if data.get('due_date'):
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        
        # Create new task
        task = Task(
            id=str(uuid.uuid4()),
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            due_date=due_date,
            contact_id=data['contact_id'],
            assigned_to=data.get('assigned_to')
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.json
    
    try:
        if 'title' in data:
            task.title = data['title']
        
        if 'description' in data:
            task.description = data['description']
        
        if 'status' in data:
            task.status = data['status']
            
        if 'priority' in data:
            task.priority = data['priority']
        
        if 'due_date' in data and data['due_date']:
            task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        elif 'due_date' in data and data['due_date'] is None:
            task.due_date = None
            
        if 'assigned_to' in data:
            task.assigned_to = data['assigned_to']
        
        db.session.commit()
        
        return jsonify(task.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 