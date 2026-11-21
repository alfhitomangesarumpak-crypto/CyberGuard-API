from flask import Blueprint
from app.controllers.incident_controller import IncidentController

incident_bp = Blueprint('incidents', __name__, url_prefix='/api/incidents')

incident_bp.route('', methods=['GET'])(IncidentController.get_all)
incident_bp.route('/<int:incident_id>', methods=['GET'])(IncidentController.get_by_id)
incident_bp.route('', methods=['POST'])(IncidentController.create)
incident_bp.route('/<int:incident_id>', methods=['PUT'])(IncidentController.update)
incident_bp.route('/<int:incident_id>', methods=['DELETE'])(IncidentController.delete)