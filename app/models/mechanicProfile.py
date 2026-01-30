# app/models/mechanic_profile.py
from datetime import datetime
from app import db  # ← assuming db is imported from app/__init__.py
# or alternatively: from flask_sqlalchemy import SQLAlchemy → db = SQLAlchemy()

class MechanicProfile(db.Model):
    """
    Mechanic profile model - extends basic user with mechanic/garage specific information
    One-to-one relationship with User (usually)
    """
    __tablename__ = 'mechanic_profiles'
    __table_args__ = {
        'extend_existing': True,   # ← This is the key line
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    garage_name = db.Column(db.String(120), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Core business information
    garage_name = db.Column(db.String(120), nullable=False)
    garage_description = db.Column(db.Text, nullable=True)
    
    # Location & contact
    location = db.Column(db.String(200), nullable=False)              # e.g. "Westlands, Nairobi"
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    whatsapp_number = db.Column(db.String(20), nullable=True)
    
    # Business details
    years_of_experience = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    
    # Working hours / availability (simple string for MVP)
    working_hours = db.Column(db.String(200), nullable=True)          # e.g. "Mon-Sat 8AM-6PM"
    
    # Media / branding
    profile_photo_url = db.Column(db.String(255), nullable=True)
    garage_photo_urls = db.Column(db.JSON, default=list, nullable=True)  # list of image URLs
    
    # Stats / performance
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    completed_bookings = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('mechanic_profile', uselist=False), lazy='joined')
    
    # Optional: services offered (many-to-many relationship - create association table if needed)
    # services = db.relationship('Service', secondary='mechanic_services', backref='mechanics')

    def __repr__(self):
        return f"<MechanicProfile {self.garage_name} - User:{self.user_id}>"

    def to_dict(self, include_user=False):
        """Helper for API responses"""
        data = {
            'id': self.id,
            'garage_name': self.garage_name,
            'location': self.location,
            'is_verified': self.is_verified,
            'is_available': self.is_available,
            'rating': round(self.rating, 1) if self.rating else 0.0,
            'total_reviews': self.total_reviews,
            'completed_bookings': self.completed_bookings,
            'profile_photo_url': self.profile_photo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_user and self.user:
            data['user'] = self.user.to_dict(only_basic=True)
            
        return data