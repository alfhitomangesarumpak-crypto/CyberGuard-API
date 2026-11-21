from datetime import datetime, timezone
from app.extensions import db

class Incident(db.Model):
    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    incident_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='open')
    description = db.Column(db.Text, nullable=True)
    reported_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    responses = db.relationship('IncidentResponse', backref='incident', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'asset_name': self.asset.asset_name if self.asset else None,
            'reported_by': self.reported_by,
            'reporter_username': self.reporter.username if self.reporter else None,
            'title': self.title,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'status': self.status,
            'description': self.description,
            'reported_at': self.reported_at.isoformat() if self.reported_at else None
        }