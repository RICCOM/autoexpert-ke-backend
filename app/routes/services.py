# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app import db
# # from app.models.service import Service  # ← uncomment when model exists

# bp = Blueprint('services', __name__)

# @bp.route('/', methods=['GET'])
# def list_services():
#     # Example: return all services (add pagination/filtering later)
#     # services = Service.query.all()
#     # return jsonify([s.to_dict() for s in services]), 200
    
#     # Placeholder until model exists
#     return jsonify({
#         "services": [
#             {"id": 1, "title": "Car Wash", "price": 1500, "duration": "45 min"},
#             {"id": 2, "title": "Oil Change", "price": 3500, "duration": "30 min"}
#         ]
#     }), 200


# @bp.route('/', methods=['POST'])
# @jwt_required()
# def create_service():
#     data = request.get_json()
    
#     required = ['title', 'description', 'price', 'duration']
#     if not all(k in data for k in required):
#         return jsonify({'error': 'Missing required fields'}), 400
    
#     # service = Service(
#     #     title=data['title'],
#     #     description=data['description'],
#     #     price=data['price'],
#     #     duration=data['duration'],
#     #     provider_id=get_jwt_identity()  # assuming service provider
#     # )
#     # db.session.add(service)
#     # db.session.commit()
    
#     # Placeholder response
#     return jsonify({
#         'message': 'Service created (placeholder)',
#         'service': data
#     }), 201


# @bp.route('/<int:service_id>', methods=['GET'])
# def get_service(service_id):
#     # service = Service.query.get_or_404(service_id)
#     # return jsonify(service.to_dict()), 200
    
#     return jsonify({
#         "id": service_id,
#         "title": "Sample Service",
#         "price": 2000,
#         "description": "Placeholder service details"
#     }), 200
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.service import Service
from app.models.user import User

bp = Blueprint('services', __name__, url_prefix='/api/services')


@bp.route('', methods=['GET', 'OPTIONS'])
def get_services():
    """Get all active services"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        services = Service.query.filter_by(is_active=True).all()
        return jsonify([service.to_dict() for service in services]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:service_id>', methods=['GET', 'OPTIONS'])
def get_service(service_id):
    """Get a specific service"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        service = Service.query.get(service_id)
        if not service:
            return jsonify({'error': 'Service not found'}), 404
        
        return jsonify(service.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500