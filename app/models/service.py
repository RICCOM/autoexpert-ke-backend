# from app import db
# from datetime import datetime

# class Service(db.Model):
#     __tablename__ = 'services'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     base_price = db.Column(db.Float, nullable=False)
#     icon = db.Column(db.String(50))
#     category = db.Column(db.String(50))
#     is_active = db.Column(db.Boolean, default=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description,
#             'base_price': self.base_price,
#             'icon': self.icon,
#             'category': self.category
#         }
from app import db
from datetime import datetime

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(50))
    category = db.Column(db.String(50))
    estimated_duration = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='service', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'base_price': self.base_price,
            'icon': self.icon,
            'category': self.category,
            'estimated_duration': self.estimated_duration,
            'is_active': self.is_active
        }