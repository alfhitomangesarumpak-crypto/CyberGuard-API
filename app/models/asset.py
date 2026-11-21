from datetime import datetime, timezone
from app.extensions import db

class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), unique=True, nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)
    criticality = db.Column(db.String(20), nullable=False, default='medium')
    owner_department = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    vulnerabilities = db.relationship('Vulnerability', backref='asset', lazy=True, cascade='all, delete-orphan')
    incidents = db.relationship('Incident', backref='asset', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'asset_name': self.asset_name,
            'ip_address': self.ip_address,
            'asset_type': self.asset_type,
            'criticality': self.criticality,
            'owner_department': self.owner_department,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }