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
#     from app.routes import auth, users, services, bookings, chat, payments
#     app.register_blueprint(auth.bp, url_prefix='/api/auth')
#     app.register_blueprint(users.bp, url_prefix='/api/users')
#     app.register_blueprint(services.bp, url_prefix='/api/services')
#     app.register_blueprint(bookings.bp, url_prefix='/api/bookings')
#     app.register_blueprint(chat.bp, url_prefix='/api/chat')
#     app.register_blueprint(payments.bp, url_prefix='/api/payments')
    
#     # Register socket handlers
#     from app.sockets import chat_handlers
    
#     return app
# app = create_app()
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS
# from flask_socketio import SocketIO
# from app.config import config
# import os

# # Initialize extensions
# db = SQLAlchemy()
# migrate = Migrate()
# jwt = JWTManager()
# socketio = SocketIO(
#     cors_allowed_origins="*",
#     async_mode='eventlet',
#     logger=True,
#     engineio_logger=True
# )


# def create_app(config_name=None):
#     """Application factory pattern"""
    
#     if config_name is None:
#         config_name = os.environ.get('FLASK_ENV', 'development')
    
#     app = Flask(__name__)
#     app.config.from_object(config[config_name])
    
#     # Ensure upload folder exists
#     os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    
#     # Initialize extensions with app
#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)
    
#     # Configure CORS
#     CORS(app, resources={
#         r"/api/*": {
#             "origins": app.config['FRONTEND_URL'],
#             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#             "allow_headers": ["Content-Type", "Authorization"],
#             "expose_headers": ["Content-Type", "Authorization"],
#             "supports_credentials": True
#         }
#     })
    
#     socketio.init_app(app)
    
#     # Register blueprints
#     from app.routes import auth, users, services, bookings, chat, payments
    
#     app.register_blueprint(auth.bp)
#     app.register_blueprint(users.bp)
#     app.register_blueprint(services.bp)
#     app.register_blueprint(bookings.bp)
#     app.register_blueprint(chat.bp)
#     app.register_blueprint(payments.bp)
    
#     # Register socket event handlers
#     from app.sockets import chat_handlers
#     chat_handlers.register_handlers(socketio)
    
#     # Register error handlers
#     register_error_handlers(app)
    
#     # Health check endpoint
#     @app.route('/health')
#     def health_check():
#         return {'status': 'healthy'}, 200
    
#     @app.route('/')
#     def index():
#         return {
#             'message': 'AutoExpert KE API',
#             'version': '1.0.0',
#             'status': 'running'
#         }, 200
    
#     return app


# def register_error_handlers(app):
#     """Register error handlers"""
    
#     @app.errorhandler(404)
#     def not_found(error):
#         return {'error': 'Resource not found'}, 404
    
#     @app.errorhandler(500)
#     def internal_error(error):
#         db.session.rollback()
#         return {'error': 'Internal server error'}, 500
    
#     @app.errorhandler(400)
#     def bad_request(error):
#         return {'error': 'Bad request'}, 400
    
#     @app.errorhandler(403)
#     def forbidden(error):
#         return {'error': 'Forbidden'}, 403

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from app.config import config
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()


def create_app(config_name=None):
    """Application factory pattern"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ensure upload folder exists
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['FRONTEND_URL'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Only initialize SocketIO if not running in CLI mode
    if not app.config.get('TESTING'):
        try:
            socketio.init_app(
                app,
                cors_allowed_origins="*",
                async_mode='eventlet',
                logger=False,
                engineio_logger=False
            )
            
            # Register socket event handlers
            from app.sockets import chat_handlers
            chat_handlers.register_handlers(socketio)
        except:
            # If eventlet is not available or in CLI mode, skip SocketIO
            pass
    
    # Register blueprints
    from app.routes import auth, users, services, bookings, chat, payments
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(services.bp)
    app.register_blueprint(bookings.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(payments.bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    @app.route('/')
    def index():
        return {
            'message': 'AutoExpert KE API',
            'version': '1.0.0',
            'status': 'running'
        }, 200
    
    return app


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden'}, 403