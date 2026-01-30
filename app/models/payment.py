# from app import db
# from datetime import datetime

# class Payment(db.Model):
#     __tablename__ = 'payments'
    
#     id = db.Column(db.Integer, primary_key=True)
#     booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
#     amount = db.Column(db.Float, nullable=False)
#     payment_method = db.Column(db.String(50), default='mpesa')
#     transaction_id = db.Column(db.String(100), unique=True)
#     phone_number = db.Column(db.String(20))
#     status = db.Column(db.String(20), default='pending')  # pending, completed, failed
#     mpesa_receipt = db.Column(db.String(100))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'booking_id': self.booking_id,
#             'amount': self.amount,
#             'payment_method': self.payment_method,
#             'transaction_id': self.transaction_id,
#             'status': self.status,
#             'mpesa_receipt': self.mpesa_receipt,
#             'created_at': self.created_at.isoformat(),
#         }

# class Review(db.Model):
#     __tablename__ = 'reviews'
    
#     id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     mechanic_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
#     rating = db.Column(db.Integer, nullable=False)  # 1-5
#     comment = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     booking = db.relationship('Booking', backref='review')
from app import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='mpesa')
    transaction_id = db.Column(db.String(100), unique=True)
    checkout_request_id = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')
    mpesa_receipt = db.Column(db.String(100))
    result_code = db.Column(db.String(10))
    result_desc = db.Column(db.String(255))
    callback_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'phone_number': self.phone_number,
            'status': self.status,
            'mpesa_receipt': self.mpesa_receipt,
            'created_at': self.created_at.isoformat(),
        }


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': f"{self.customer.first_name} {self.customer.last_name}",
            'mechanic_id': self.mechanic_id,
            'booking_id': self.booking_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
        }