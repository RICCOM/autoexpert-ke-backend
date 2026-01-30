# from app import db
# from datetime import datetime

# class Booking(db.Model):
#     __tablename__ = 'bookings'
    
#     id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     mechanic_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
#     status = db.Column(db.String(20), default='pending')  # pending, accepted, in_progress, completed, cancelled
#     description = db.Column(db.Text, nullable=False)
#     scheduled_at = db.Column(db.DateTime)
#     completed_at = db.Column(db.DateTime)
#     price = db.Column(db.Float)
#     payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # Relationships
#     service = db.relationship('Service', backref='bookings')
#     chat_room = db.relationship('ChatRoom', backref='booking', uselist=False, cascade='all, delete-orphan')
#     payment = db.relationship('Payment', backref='booking', uselist=False, cascade='all, delete-orphan')
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'customer_id': self.customer_id,
#             'mechanic_id': self.mechanic_id,
#             'service': self.service.to_dict() if self.service else None,
#             'status': self.status,
#             'description': self.description,
#             'price': self.price,
#             'payment_status': self.payment_status,
#             'created_at': self.created_at.isoformat(),
#         }
from app import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    description = db.Column(db.Text, nullable=False)
    vehicle_info = db.Column(db.JSON)
    scheduled_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    price = db.Column(db.Float)
    payment_status = db.Column(db.String(20), default='pending')
    cancellation_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    chat_room = db.relationship('ChatRoom', backref='booking', uselist=False, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='booking', uselist=False, cascade='all, delete-orphan')
    review = db.relationship('Review', backref='booking', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'customer_id': self.customer_id,
            'mechanic_id': self.mechanic_id,
            'service_id': self.service_id,
            'status': self.status,
            'description': self.description,
            'vehicle_info': self.vehicle_info,
            'price': self.price,
            'payment_status': self.payment_status,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'created_at': self.created_at.isoformat(),
        }
        
        if include_details:
            data['customer'] = self.customer.to_dict() if self.customer else None
            data['mechanic'] = self.mechanic.to_dict(include_profile=True) if self.mechanic else None
            data['service'] = self.service.to_dict() if self.service else None
            data['chat_room_id'] = self.chat_room.id if self.chat_room else None
        
        return data