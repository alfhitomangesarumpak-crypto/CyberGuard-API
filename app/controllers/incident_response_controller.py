from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import IncidentResponse, Incident, User
from app.schemas import IncidentResponseSchema

response_schema = IncidentResponseSchema()

class IncidentResponseController:
    @staticmethod
    def get_all():
        incident_id = request.args.get('incident_id')
        query = IncidentResponse.query
        if incident_id:
            query = query.filter_by(incident_id=incident_id)
        responses = query.all()
        return jsonify({
            "status": "success",
            "total": len(responses),
            "data": [r.to_dict() for r in responses]
        }), 200

    @staticmethod
    def get_by_id(response_id):
        resp = db.session.get(IncidentResponse, response_id)
        if not resp:
            return jsonify({"status": "error", "message": "Incident response tidak ditemukan"}), 404
        return jsonify({"status": "success", "data": resp.to_dict()}), 200

    @staticmethod
    def create():
        try:
            data = response_schema.load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({"status": "error", "errors": err.messages}), 400

        if not db.session.get(Incident, data['incident_id']):
            return jsonify({"status": "error", "message": "Incident ID tidak ditemukan"}), 404
        if not db.session.get(User, data['responder_id']):
            return jsonify({"status": "error", "message": "User responder tidak ditemukan"}), 404

        new_resp = IncidentResponse(**data)
        db.session.add(new_resp)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Tindakan respons insiden berhasil dicatat",
            "data": new_resp.to_dict()
        }), 201

    @staticmethod
    def update(response_id):
        resp = db.session.get(IncidentResponse, response_id)
        if not resp:
            return jsonify({"status": "error", "message": "Incident response tidak ditemukan"}), 404

        try:
            data = response_schema.load(request.get_json() or {}, partial=True)
        except ValidationError as err:
            return jsonify({"status": "error", "errors": err.messages}), 400

        for key, value in data.items():
            setattr(resp, key, value)

        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Tindakan respons berhasil diperbarui",
            "data": resp.to_dict()
        }), 200

    @staticmethod
    def delete(response_id):
        resp = db.session.get(IncidentResponse, response_id)
        if not resp:
            return jsonify({"status": "error", "message": "Incident response tidak ditemukan"}), 404

        db.session.delete(resp)
        db.session.commit()
        return jsonify({"status": "success", "message": "Tindakan respons berhasil dihapus"}), 200