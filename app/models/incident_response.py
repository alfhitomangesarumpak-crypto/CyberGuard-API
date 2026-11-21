from datetime import datetime, timezone
from app.extensions import db

class IncidentResponse(db.Model):
    __tablename__ = 'incident_responses'

    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    responder_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action_taken = db.Column(db.String(150), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'responder_id': self.responder_id,
            'responder_username': self.responder.username if self.responder else None,
            'action_taken': self.action_taken,
            'notes': self.notes,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }