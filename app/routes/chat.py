from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
# from app.models.message import Message  # ← uncomment when model exists

bp = Blueprint('chat', __name__)

@bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    user_id = get_jwt_identity()
    # Logic to get list of conversations for this user
    
    # Placeholder
    return jsonify({
        "conversations": [
            {"id": 1, "with_user_id": 42, "last_message": "Hey, is the car ready?", "timestamp": "2025-10-15T14:30:00"},
            {"id": 2, "with_user_id": 7, "last_message": "Payment confirmed", "timestamp": "2025-10-14T09:15:00"}
        ]
    }), 200


@bp.route('/<int:conversation_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    # user_id = get_jwt_identity()
    # messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
    
    # Placeholder
    return jsonify({
        "conversation_id": conversation_id,
        "messages": [
            {"sender_id": 42, "content": "When will my car be ready?", "timestamp": "2025-10-15T14:28:00"},
            {"sender_id": user_id, "content": "In about 30 minutes", "timestamp": "2025-10-15T14:30:00"}
        ]
    }), 200


@bp.route('/<int:conversation_id>/messages', methods=['POST'])
@jwt_required()
def send_message(conversation_id):
    data = request.get_json()
    if 'content' not in data or not data['content'].strip():
        return jsonify({'error': 'Message content required'}), 400
    
    user_id = get_jwt_identity()
    
    # message = Message(
    #     conversation_id=conversation_id,
    #     sender_id=user_id,
    #     content=data['content']
    # )
    # db.session.add(message)
    # db.session.commit()
    
    # In real app: emit via socketio
    
    return jsonify({
        'message': 'Message sent',
        'content': data['content']
    }), 201