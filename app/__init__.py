from flask import Flask, jsonify
from config import Config
from app.extensions import db, migrate
from app.routes import register_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inisialisasi ekstensi
    db.init_app(app)
    migrate.init_app(app, db)
   

    # Impor models agar terdeteksi oleh Flask-Migrate
    from app import models

    # Daftarkan semua API routes
    register_routes(app)

    # Global Error Handlers (Format error konsisten - Soal 3)
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"status": "error", "message": "Bad Request", "details": str(error.description)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"status": "error", "message": "Unauthorized", "details": str(error.description)}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"status": "error", "message": "HTTP Method tidak diizinkan"}), 405

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    # Endpoint root & health-check sederhana
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "app": "CyberGuard-API",
            "status": "running",
            "endpoints": [
                "/api/health",
                "/api/users",
                "/api/assets",
                "/api/vulnerabilities",
                "/api/incidents",
                "/api/incident-responses"
            ]
        }), 200

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "success", "message": "CyberGuard API is running!"}), 200

    return app