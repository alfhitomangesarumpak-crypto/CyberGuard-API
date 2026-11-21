from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import Asset
from app.schemas import AssetSchema

asset_schema = AssetSchema()

class AssetController:
    @staticmethod
    def get_all():
        criticality = request.args.get('criticality')
        query = Asset.query
        if criticality:
            query = query.filter_by(criticality=criticality)
        assets = query.all()
        return jsonify({
            "status": "success",
            "total": len(assets),
            "data": [a.to_dict() for a in assets]
        }), 200

    @staticmethod
    def get_by_id(asset_id):
        asset = db.session.get(Asset, asset_id)
        if not asset:
            return jsonify({"status": "error", "message": "Asset tidak ditemukan"}), 404
        return jsonify({"status": "success", "data": asset.to_dict()}), 200

    @staticmethod
    def create():
        try:
            data = asset_schema.load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({"status": "error", "errors": err.messages}), 400

        if Asset.query.filter_by(ip_address=str(data['ip_address'])).first():
            return jsonify({"status": "error", "message": "IP Address sudah terdaftar pada asset lain"}), 409

        new_asset = Asset(
            asset_name=data['asset_name'],
            ip_address=str(data['ip_address']),
            asset_type=data['asset_type'],
            criticality=data['criticality'],
            owner_department=data['owner_department']
        )
        db.session.add(new_asset)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Asset berhasil ditambahkan",
            "data": new_asset.to_dict()
        }), 201

    @staticmethod
    def update(asset_id):
        asset = db.session.get(Asset, asset_id)
        if not asset:
            return jsonify({"status": "error", "message": "Asset tidak ditemukan"}), 404

        try:
            data = asset_schema.load(request.get_json() or {}, partial=True)
        except ValidationError as err:
            return jsonify({"status": "error", "errors": err.messages}), 400

        for key, value in data.items():
            setattr(asset, key, str(value) if key == 'ip_address' else value)

        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Asset berhasil diperbarui",
            "data": asset.to_dict()
        }), 200

    @staticmethod
    def delete(asset_id):
        asset = db.session.get(Asset, asset_id)
        if not asset:
            return jsonify({"status": "error", "message": "Asset tidak ditemukan"}), 404

        db.session.delete(asset)
        db.session.commit()
        return jsonify({"status": "success", "message": "Asset berhasil dihapus"}), 200