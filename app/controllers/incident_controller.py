from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import Incident, Asset, User
from app.schemas import IncidentSchema

incident_schema = IncidentSchema()

class IncidentController:
    @staticmethod
    def get_all():
        status = request.args.get('status')
        severity = request.args.get('severity')
        query = Incident.query
        if status:
            query = query.filter_by(status=status)
        if severity:
            query = query.filter_by(severity=severity)
        incidents = query.all()
        return jsonify({
            "status": "success",
            "total": len(incidents),
            "data": [i.to_dict() for i in incidents]
        }), 200

    @staticmethod
    def get_by_id(incident_id):
        incident = db.session.get(Incident, incident_id)
        if not incident:
            return jsonify({"status": "error", "message": "Incident tidak ditemukan"}), 404
        return jsonify({"status": "success", "data": incident.to_dict()}), 200

    @staticmethod
    def create():
        try:
            data = incident_schema.load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({"status": "error", "errors": err.messages}), 400

        if not db.session.get(Asset, data['asset_id']):
            return jsonify({"status": "error", "message": "Asset ID tidak ditemukan"}), 404
        if not db.session.get(User, data['reported_by']):
            return jsonify({"status": "error", "message": "User pelapor (reported_by) tidak ditemukan"}), 404

        new_incident = Incident(**data)
        db.session.add(new_incident)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Incident berhasil dilaporkan",
            "data": new_incident.to_dict()
        }), 201

    @staticmethod
    def update(incident_id):
        incident = db.session.get(Incident, incident_id)
        if not incident:
            return jsonify({"status": "error", "message": "Incident tidak ditemukan"}), 404

        try:
            data = incident_schema.load(request.get_json() or {}, partial=True)
        except ValidationError as err:
            return jsonify({"status": "error", "errors": err.messages}), 400

        if 'asset_id' in data and not db.session.get(Asset, data['asset_id']):
            return jsonify({"status": "error", "message": "Asset ID tidak ditemukan"}), 404
        if 'reported_by' in data and not db.session.get(User, data['reported_by']):
            return jsonify({"status": "error", "message": "User pelapor tidak ditemukan"}), 404

        for key, value in data.items():
            setattr(incident, key, value)

        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Incident berhasil diperbarui",
            "data": incident.to_dict()
        }), 200

    @staticmethod
    def delete(incident_id):
        incident = db.session.get(Incident, incident_id)
        if not incident:
            return jsonify({"status": "error", "message": "Incident tidak ditemukan"}), 404

        db.session.delete(incident)
        db.session.commit()
        return jsonify({"status": "success", "message": "Incident berhasil dihapus"}), 200