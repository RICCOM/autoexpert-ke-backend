from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token
from app import db
from app.models.chat import ChatRoom, Message
from app.models.booking import Booking
from datetime import datetime


def register_handlers(socketio):
    """Register Socket.IO event handlers"""
    
    @socketio.on('connect')
    def handle_connect(auth):
        """Handle client connection"""
        try:
            # Verify JWT token
            token = auth.get('token') if auth else None
            if not token:
                disconnect()
                return False
            
            # Decode token
            decoded = decode_token(token)
            user_id = decoded['sub']
            
            emit('connected', {'message': 'Connected to chat server'})
            print(f"User {user_id} connected with session {request.sid}")
            
        except Exception as e:
            print(f"Connection error: {str(e)}")
            disconnect()
            return False
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        try:
            print(f"Client disconnected: {request.sid}")
        except Exception as e:
            print(f"Disconnect error: {str(e)}")
    
    @socketio.on('join_room')
    def handle_join_room(data):
        """Handle user joining a chat room"""
        try:
            room_id = data.get('room_id')
            if not room_id:
                emit('error', {'message': 'Room ID required'})
                return
            
            # Verify room exists
            room = ChatRoom.query.get(room_id)
            if not room:
                emit('error', {'message': 'Room not found'})
                return
            
            # Join Socket.IO room
            join_room(str(room_id))
            emit('joined_room', {'room_id': room_id})
            print(f"User joined room {room_id}")
            
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('leave_room')
    def handle_leave_room(data):
        """Handle user leaving a chat room"""
        try:
            room_id = data.get('room_id')
            if room_id:
                leave_room(str(room_id))
                emit('left_room', {'room_id': room_id})
                print(f"User left room {room_id}")
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('send_message')
    def handle_send_message(data):
        """Handle sending a message"""
        try:
            room_id = data.get('room_id')
            content = data.get('content')
            
            if not room_id or not content:
                emit('error', {'message': 'Room ID and content required'})
                return
            
            # Get JWT token from auth
            token = request.args.get('token')
            if not token:
                emit('error', {'message': 'Unauthorized'})
                return
            
            decoded = decode_token(token)
            user_id = decoded['sub']
            
            # Verify room exists
            room = ChatRoom.query.get(room_id)
            if not room:
                emit('error', {'message': 'Room not found'})
                return
            
            # Verify user has access
            booking = room.booking
            if booking.customer_id != user_id and booking.mechanic_id != user_id:
                emit('error', {'message': 'Unauthorized'})
                return
            
            # Create message
            message = Message(
                chat_room_id=room_id,
                sender_id=user_id,
                content=content,
                message_type='text'
            )
            
            db.session.add(message)
            room.last_message_at = datetime.utcnow()
            db.session.commit()
            
            # Broadcast message to room
            message_data = message.to_dict()
            emit('new_message', message_data, room=str(room_id))
            
            print(f"Message sent in room {room_id}")
            
        except Exception as e:
            db.session.rollback()
            emit('error', {'message': str(e)})
            print(f"Send message error: {str(e)}")
    
    @socketio.on('typing')
    def handle_typing(data):
        """Handle typing indicator"""
        try:
            room_id = data.get('room_id')
            is_typing = data.get('is_typing', False)
            
            if room_id:
                emit('user_typing', {
                    'room_id': room_id,
                    'is_typing': is_typing
                }, room=str(room_id), include_self=False)
                
        except Exception as e:
            print(f"Typing indicator error: {str(e)}")