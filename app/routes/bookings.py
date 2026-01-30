# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app import db
# from app.models.booking import Booking
# from app.models.service import Service
# from app.models.chat import ChatRoom
# from datetime import datetime

# bp = Blueprint('bookings', __name__)

# @bp.route('/', methods=['POST'])
# @jwt_required()
# def create_booking():
#     user_id = get_jwt_identity()
#     data = request.get_json()
    
#     required_fields = ['service_id', 'description']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Missing required fields'}), 400
    
#     service = Service.query.get(data['service_id'])
#     if not service:
#         return jsonify({'error': 'Service not found'}), 404
    
#     booking = Booking(
#         customer_id=user_id,
#         service_id=data['service_id'],
#         description=data['description'],
#         price=service.base_price,
#         scheduled_at=datetime.fromisoformat(data.get('scheduled_at')) if data.get('scheduled_at') else None
#     )
    
#     db.session.add(booking)
#     db.session.commit()
    
#     # Create chat room for booking
#     chat_room = ChatRoom(booking_id=booking.id)
#     db.session.add(chat_room)
#     db.session.commit()
    
#     return jsonify({
#         'message': 'Booking created successfully',
#         'booking': booking.to_dict()
#     }), 201

# @bp.route('/', methods=['GET'])
# @jwt_required()
# def get_bookings():
#     user_id = get_jwt_identity()
    
#     bookings = Booking.query.filter(
#         (Booking.customer_id == user_id) | (Booking.mechanic_id == user_id)
#     ).order_by(Booking.created_at.desc()).all()
    
#     return jsonify([booking.to_dict() for booking in bookings]), 200

# @bp.route('/<int:booking_id>', methods=['GET'])
# @jwt_required()
# def get_booking(booking_id):
#     user_id = get_jwt_identity()
    
#     booking = Booking.query.get(booking_id)
#     if not booking:
#         return jsonify({'error': 'Booking not found'}), 404
    
#     if booking.customer_id != user_id and booking.mechanic_id != user_id:
#         return jsonify({'error': 'Unauthorized'}), 403
    
#     return jsonify(booking.to_dict()), 200

# @bp.route('/<int:booking_id>/accept', methods=['POST'])
# @jwt_required()
# def accept_booking(booking_id):
#     user_id = get_jwt_identity()
    
#     booking = Booking.query.get(booking_id)
#     if not booking:
#         return jsonify({'error': 'Booking not found'}), 404
    
#     if booking.status != 'pending':
#         return jsonify({'error': 'Booking cannot be accepted'}),
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.booking import Booking
from app.models.service import Service
from app.models.chat import ChatRoom
from app.models.user import User
from datetime import datetime

bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')


@bp.route('', methods=['POST', 'OPTIONS'])
@jwt_required()
def create_booking():
    """Create a new booking"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['service_id', 'description']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Verify service exists
        service = Service.query.get(data['service_id'])
        if not service or not service.is_active:
            return jsonify({'error': 'Service not found or inactive'}), 404
        
        # Create booking
        booking = Booking(
            customer_id=user_id,
            service_id=data['service_id'],
            description=data['description'],
            vehicle_info=data.get('vehicle_info'),
            price=service.base_price,
            scheduled_at=datetime.fromisoformat(data['scheduled_at']) if data.get('scheduled_at') else None
        )
        
        db.session.add(booking)
        db.session.flush()
        
        # Create chat room for booking
        chat_room = ChatRoom(booking_id=booking.id)
        db.session.add(chat_room)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_bookings():
    """Get all bookings for current user"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get bookings based on user role
        if user.role == 'customer':
            bookings = Booking.query.filter_by(customer_id=user_id).order_by(Booking.created_at.desc()).all()
        elif user.role == 'mechanic':
            bookings = Booking.query.filter(
                (Booking.mechanic_id == user_id) | 
                (Booking.status == 'pending')
            ).order_by(Booking.created_at.desc()).all()
        else:  # admin
            bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        
        return jsonify([booking.to_dict(include_details=True) for booking in bookings]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:booking_id>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_booking(booking_id):
    """Get a specific booking"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        user_id = get_jwt_identity()
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check authorization
        user = User.query.get(user_id)
        if user.role not in ['admin'] and booking.customer_id != user_id and booking.mechanic_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        return jsonify(booking.to_dict(include_details=True)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:booking_id>/accept', methods=['POST', 'OPTIONS'])
@jwt_required()
def accept_booking(booking_id):
    """Accept a booking (mechanics only)"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role != 'mechanic':
            return jsonify({'error': 'Only mechanics can accept bookings'}), 403
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        if booking.status != 'pending':
            return jsonify({'error': 'Booking is not in pending status'}), 400
        
        booking.mechanic_id = user_id
        booking.status = 'accepted'
        db.session.commit()
        
        return jsonify({
            'message': 'Booking accepted successfully',
            'booking': booking.to_dict(include_details=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500