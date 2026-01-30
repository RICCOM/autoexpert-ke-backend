# from app import db
# from datetime import datetime
# import bcrypt

# class User(db.Model):
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False, index=True)
#     phone = db.Column(db.String(20), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     role = db.Column(db.String(20), nullable=False, default='customer')  # customer, mechanic, admin
#     is_verified = db.Column(db.Boolean, default=False)
#     is_active = db.Column(db.Boolean, default=True)
#     profile_image = db.Column(db.String(255))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # Relationships
#     mechanic_profile = db.relationship('MechanicProfile', backref='user', uselist=False, cascade='all, delete-orphan')
#     bookings = db.relationship('Booking', backref='customer', foreign_keys='Booking.customer_id')
#     messages_sent = db.relationship('Message', backref='sender', foreign_keys='Message.sender_id')
#     reviews = db.relationship('Review', backref='customer', foreign_keys='Review.customer_id')
    
#     def set_password(self, password):
#         self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
#     def check_password(self, password):
#         return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'email': self.email,
#             'phone': self.phone,
#             'first_name': self.first_name,
#             'last_name': self.last_name,
#             'role': self.role,
#             'is_verified': self.is_verified,
#             'profile_image': self.profile_image,
#             'created_at': self.created_at.isoformat(),
#         }

# class MechanicProfile(db.Model):
#     __tablename__ = 'mechanic_profiles'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
#     specialization = db.Column(db.String(100))
#     years_experience = db.Column(db.Integer)
#     certification = db.Column(db.String(255))
#     bio = db.Column(db.Text)
#     hourly_rate = db.Column(db.Float)
#     is_available = db.Column(db.Boolean, default=True)
#     rating = db.Column(db.Float, default=0.0)
#     total_reviews = db.Column(db.Integer, default=0)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # Relationships
#     bookings = db.relationship('Booking', backref='mechanic', foreign_keys='Booking.mechanic_id')
#     reviews = db.relationship('Review', backref='mechanic', foreign_keys='Review.mechanic_id'
from app import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    mechanic_profile = db.relationship('MechanicProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    customer_bookings = db.relationship('Booking', backref='customer', foreign_keys='Booking.customer_id', cascade='all, delete-orphan')
    mechanic_bookings = db.relationship('Booking', backref='mechanic', foreign_keys='Booking.mechanic_id')
    messages_sent = db.relationship('Message', backref='sender', foreign_keys='Message.sender_id', cascade='all, delete-orphan')
    customer_reviews = db.relationship('Review', backref='customer', foreign_keys='Review.customer_id', cascade='all, delete-orphan')
    mechanic_reviews = db.relationship('Review', backref='mechanic', foreign_keys='Review.mechanic_id')
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self, include_profile=False):
        data = {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'role': self.role,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat(),
        }
        
        if include_profile and self.role == 'mechanic' and self.mechanic_profile:
            data['mechanic_profile'] = self.mechanic_profile.to_dict()
        
        return data


class MechanicProfile(db.Model):
    __tablename__ = 'mechanic_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    specialization = db.Column(db.String(100))
    years_experience = db.Column(db.Integer)
    certification = db.Column(db.String(255))
    bio = db.Column(db.Text)
    hourly_rate = db.Column(db.Float, default=500.0)
    is_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    total_jobs = db.Column(db.Integer, default=0)
    verification_status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'specialization': self.specialization,
            'years_experience': self.years_experience,
            'certification': self.certification,
            'bio': self.bio,
            'hourly_rate': self.hourly_rate,
            'is_available': self.is_available,
            'rating': round(self.rating, 1),
            'total_reviews': self.total_reviews,
            'total_jobs': self.total_jobs,
            'verification_status': self.verification_status,
        }
    
    def update_rating(self):
        from app.models.payment import Review
        reviews = Review.query.filter_by(mechanic_id=self.user_id).all()
        
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.rating = total_rating / len(reviews)
            self.total_reviews = len(reviews)
        else:
            self.rating = 0.0
            self.total_reviews = 0
        
        db.session.commit()
