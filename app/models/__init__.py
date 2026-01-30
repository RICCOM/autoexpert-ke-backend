# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS
# from flask_socketio import SocketIO
# from app.config import Config

# db = SQLAlchemy()
# migrate = Migrate()
# jwt = JWTManager()
# socketio = SocketIO(cors_allowed_origins="*")

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)
    
#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)
#     CORS(app, resources={r"/api/*": {"origins": app.config['FRONTEND_URL']}})
#     socketio.init_app(app)
    
#     # Register blueprints
#     from app.routes import auth, users, services, bookings, chat, payments, profileMechanics
#     app.register_blueprint(auth.bp, url_prefix='/api/auth')
#     app.register_blueprint(users.bp, url_prefix='/api/users')
#     app.register_blueprint(services.bp, url_prefix='/api/services')
#     app.register_blueprint(bookings.bp, url_prefix='/api/bookings')
#     app.register_blueprint(chat.bp, url_prefix='/api/chat')
#     app.register_blueprint(payments.bp, url_prefix='/api/payments')
#     app.register_blueprint(profileMechanics.bp, url_prefix='/api/profileMechanics')
    
#     # Register socket handlers
#     from app.sockets import chat_handlers
    
#     return app
from app.models.user import User, MechanicProfile
from app.models.service import Service
from app.models.booking import Booking
from app.models.chat import ChatRoom, Message
from app.models.payment import Payment, Review

__all__ = [
    'User',
    'MechanicProfile',
    'Service',
    'Booking',
    'ChatRoom',
    'Message',
    'Payment',
    'Review'
]