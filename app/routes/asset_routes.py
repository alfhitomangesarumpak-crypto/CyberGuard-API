from flask import Blueprint
from app.controllers.asset_controller import AssetController

asset_bp = Blueprint('assets', __name__, url_prefix='/api/assets')

asset_bp.route('', methods=['GET'])(AssetController.get_all)
asset_bp.route('/<int:asset_id>', methods=['GET'])(AssetController.get_by_id)
asset_bp.route('', methods=['POST'])(AssetController.create)
asset_bp.route('/<int:asset_id>', methods=['PUT'])(AssetController.update)
asset_bp.route('/<int:asset_id>', methods=['DELETE'])(AssetController.delete)