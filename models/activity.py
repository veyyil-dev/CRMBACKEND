from datetime import datetime
from database import db

class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.String(36), primary_key=True)
    contact_id = db.Column(db.String(36), db.ForeignKey('contacts.id'))
    type = db.Column(db.String(50), nullable=False)  # call, meeting, email, other
    notes = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Activity {self.type} - {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'type': self.type,
            'notes': self.notes,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 


    