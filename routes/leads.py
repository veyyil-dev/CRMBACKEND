import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db
from models.lead import Lead

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/leads', methods=['GET'])
def get_leads():
    contact_id = request.args.get('contact_id')
    status = request.args.get('status')
    
    query = Lead.query
    
    if contact_id:
        query = query.filter_by(contact_id=contact_id)
    
    if status:
        query = query.filter_by(status=status)
    
    leads = query.order_by(Lead.created_at.desc()).all()
    return jsonify([lead.to_dict() for lead in leads])

@leads_bp.route('/leads/<lead_id>', methods=['GET'])
def get_lead(lead_id):
    lead = Lead.query.get(lead_id)
    
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    
    return jsonify(lead.to_dict())

@leads_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.json
    
    # Validate required fields
    required_fields = ['contactId', 'status', 'source']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # Create new lead
        lead = Lead(
            id=str(uuid.uuid4()),
            contact_id=data['contactId'],
            status=data['status'],
            source=data['source'],
            description=data.get('description', ''),
            value=float(data.get('value', 0)),
            assigned_to=data.get('assignedTo')
        )
        
        db.session.add(lead)
        db.session.commit()
        
        return jsonify(lead.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads/<lead_id>', methods=['PUT'])
def update_lead(lead_id):
    lead = Lead.query.get(lead_id)
    
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    
    data = request.json
    
    try:
        if 'status' in data:
            lead.status = data['status']
        
        if 'source' in data:
            lead.source = data['source']
        
        if 'description' in data:
            lead.description = data['description']
        
        if 'value' in data:
            lead.value = float(data['value'])
        
        if 'assignedTo' in data:
            lead.assigned_to = data['assignedTo']
        
        db.session.commit()
        
        return jsonify(lead.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads/<lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    lead = Lead.query.get(lead_id)
    
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    
    try:
        db.session.delete(lead)
        db.session.commit()
        
        return jsonify({'message': 'Lead deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 