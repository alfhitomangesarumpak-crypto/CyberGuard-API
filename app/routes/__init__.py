from app.routes.user_routes import user_bp
from app.routes.asset_routes import asset_bp
from app.routes.vulnerability_routes import vuln_bp
from app.routes.incident_routes import incident_bp
from app.routes.incident_response_routes import response_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(asset_bp)
    app.register_blueprint(vuln_bp)
    app.register_blueprint(incident_bp)
    app.register_blueprint(response_bp)