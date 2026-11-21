from flask import Blueprint
from app.controllers.incident_response_controller import IncidentResponseController

response_bp = Blueprint('incident_responses', __name__, url_prefix='/api/incident-responses')

response_bp.route('', methods=['GET'])(IncidentResponseController.get_all)
response_bp.route('/<int:response_id>', methods=['GET'])(IncidentResponseController.get_by_id)
response_bp.route('', methods=['POST'])(IncidentResponseController.create)
response_bp.route('/<int:response_id>', methods=['PUT'])(IncidentResponseController.update)
response_bp.route('/<int:response_id>', methods=['DELETE'])(IncidentResponseController.delete)