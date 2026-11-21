from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import User
from app.schemas import UserSchema

user_schema = UserSchema()

class UserController:
    @staticmethod
    def get_all():
        users = User.query.all()
        return jsonify({
            "status": "success",
            "total": len(users),
            "data": [u.to_dict() for u in users]
        }), 200

    @staticmethod
    def get_by_id(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"status": "error", "message": "User tidak ditemukan"}), 404
        return jsonify({"status": "success", "data": user.to_dict()}), 200

    @staticmethod
    def create():
        try:
            data = user_schema.load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({"status": "error", "errors": err.messages}), 400

        if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
            return jsonify({"status": "error", "message": "Username atau email sudah terdaftar"}), 409

        new_user = User(
            username=data['username'],
            email=data['email'],
            role=data['role']
        )
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "User berhasil dibuat",
            "data": new_user.to_dict()
        }), 201

    @staticmethod
    def update(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"status": "error", "message": "User tidak ditemukan"}), 404

        try:
            data = user_schema.load(request.get_json() or {}, partial=True)
        except ValidationError as err:
            return jsonify({"status": "error", "errors": err.messages}), 400

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'role' in data:
            user.role = data['role']
        if 'password' in data:
            user.set_password(data['password'])

        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "User berhasil diperbarui",
            "data": user.to_dict()
        }), 200

    @staticmethod
    def delete(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"status": "error", "message": "User tidak ditemukan"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success", "message": "User berhasil dihapus"}), 200