from datetime import datetime
from database import db

class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.String(36), primary_key=True)
    contact_id = db.Column(db.String(36), db.ForeignKey('contacts.id'))
    status = db.Column(db.String(20), nullable=False)  # new, contacted, qualified, proposal, negotiation, closed-won, closed-lost
    source = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    value = db.Column(db.Float, default=0.0)
    assigned_to = db.Column(db.String(36))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Lead {self.id} - {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'contactId': self.contact_id,
            'status': self.status,
            'source': self.source,
            'description': self.description,
            'value': self.value,
            'assignedTo': self.assigned_to,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        } 