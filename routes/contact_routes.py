from flask import Blueprint, jsonify, request
from models import Contact
from database import db
import uuid
from datetime import datetime

contact_bp = Blueprint('contacts', __name__)

@contact_bp.route('/contacts', methods=['GET'])
def get_contacts():
    """Get all contacts"""
    contacts = Contact.query.all()
    return jsonify([contact.to_dict() for contact in contacts])

@contact_bp.route('/contacts/<contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Get a specific contact"""
    contact = Contact.query.get_or_404(contact_id)
    return jsonify(contact.to_dict())

@contact_bp.route('/contacts', methods=['POST'])
def create_contact():
    """Create a new contact"""
    data = request.get_json()
    
    # Generate UUID for new contact
    data['id'] = str(uuid.uuid4())
    
    try:
        new_contact = Contact(**data)
        db.session.add(new_contact)
        db.session.commit()
        return jsonify(new_contact.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@contact_bp.route('/contacts/<contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Update a contact"""
    contact = Contact.query.get_or_404(contact_id)
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if hasattr(contact, key):
                if key == 'last_contact' and value:
                    value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                setattr(contact, key, value)
        
        contact.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(contact.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@contact_bp.route('/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Delete a contact"""
    contact = Contact.query.get_or_404(contact_id)
    
    try:
        db.session.delete(contact)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Additional useful routes

@contact_bp.route('/contacts/search', methods=['GET'])
def search_contacts():
    """Search contacts by name, email, or company"""
    query = request.args.get('q', '')
    
    contacts = Contact.query.filter(
        db.or_(
            Contact.name.ilike(f'%{query}%'),
            Contact.email.ilike(f'%{query}%'),
            Contact.company.ilike(f'%{query}%')
        )
    ).all()
    
    return jsonify([contact.to_dict() for contact in contacts])

@contact_bp.route('/contacts/company/<company>', methods=['GET'])
def get_contacts_by_company(company):
    """Get all contacts from a specific company"""
    contacts = Contact.query.filter_by(company=company).all()
    return jsonify([contact.to_dict() for contact in contacts])

@contact_bp.route('/contacts/email/<email>', methods=['GET'])
def check_email_exists(email):
    """Check if a contact with the given email exists"""
    contact = Contact.query.filter_by(email=email).first()
    if contact:
        return jsonify({"exists": True, "contact": contact.to_dict()}), 200
    return jsonify({"exists": False}), 404 