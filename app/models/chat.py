from app import db
from datetime import datetime

class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    last_message_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    messages = db.relationship('Message', backref='chat_room', cascade='all, delete-orphan', order_by='Message.created_at')
    
    def to_dict(self, include_messages=False):
        data = {
            'id': self.id,
            'booking_id': self.booking_id,
            'is_active': self.is_active,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'unread_count': self.get_unread_count(),
            'booking': self.booking.to_dict(include_details=True) if self.booking else None,
        }
        
        if include_messages:
            data['messages'] = [msg.to_dict() for msg in self.messages]
        
        return data
    
    def get_unread_count(self, user_id=None):
        if not user_id:
            return Message.query.filter_by(chat_room_id=self.id, is_read=False).count()
        
        return Message.query.filter(
            Message.chat_room_id == self.id,
            Message.is_read == False,
            Message.sender_id != user_id
        ).count()


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    chat_room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')
    attachment_url = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'chat_room_id': self.chat_room_id,
            'sender_id': self.sender_id,
            'sender_name': f"{self.sender.first_name} {self.sender.last_name}",
            'sender_role': self.sender.role,
            'content': self.content,
            'message_type': self.message_type,
            'attachment_url': self.attachment_url,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
        }