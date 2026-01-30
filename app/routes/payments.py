from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
# from app.models.booking import Booking
# from app.models.payment import Payment

bp = Blueprint('payments', __name__)

@bp.route('/mpesa/stkpush', methods=['POST'])
@jwt_required()
def initiate_mpesa_stk_push():
    data = request.get_json()
    
    required = ['booking_id', 'phone_number', 'amount']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user_id = get_jwt_identity()
    
    # In real app: validate booking belongs to user
    # Generate STK push via Daraja API
    
    # Placeholder response
    return jsonify({
        'message': 'STK Push initiated (placeholder)',
        'checkout_request_id': 'ws_CO_123456789_202510151530',
        'booking_id': data['booking_id'],
        'amount': data['amount']
    }), 200


@bp.route('/callback', methods=['POST'])
def mpesa_callback():
    # This endpoint is called by Safaricom
    # Should be public (no JWT)
    
    data = request.get_json()
    # Process callback, update Payment/Booking status
    
    # Placeholder
    print("M-Pesa Callback received:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200


@bp.route('/booking/<int:booking_id>/status', methods=['GET'])
@jwt_required()
def get_payment_status(booking_id):
    user_id = get_jwt_identity()
    # payment = Payment.query.filter_by(booking_id=booking_id).first()
    
    # Placeholder
    return jsonify({
        "booking_id": booking_id,
        "status": "completed",  # pending, completed, failed
        "amount": 4500,
        "transaction_id": "PLK123456"
    }), 200