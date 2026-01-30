# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
#     # ── Changed this part ────────────────────────────────────────────────
#     SQLALCHEMY_DATABASE_URI = (
#         os.environ.get('DATABASE_URL')
#         or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'app.db')
#     )
#     # ──────────────────────────────────────────────────────────────────────

#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
#     JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
#     FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
    
#     # M-Pesa Configuration
#     MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
#     MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')
#     MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE')
#     MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY')
#     MPESA_CALLBACK_URL = os.environ.get('MPESA_CALLBACK_URL')
# import os
# from datetime import timedelta
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     """Base configuration"""
    
#     # Flask
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
#     # Database
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///autoexpert.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ENGINE_OPTIONS = {
#         'pool_size': 10,
#         'pool_recycle': 3600,
#         'pool_pre_ping': True,
#         'max_overflow': 20,
#     }
    
#     # JWT
#     JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400)))
#     JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
#     JWT_TOKEN_LOCATION = ['headers']
#     JWT_HEADER_NAME = 'Authorization'
#     JWT_HEADER_TYPE = 'Bearer'
    
#     # CORS
#     FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
    
#     # M-Pesa
#     MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT', 'sandbox')
#     MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
#     MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')
#     MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE')
#     MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY')
#     MPESA_CALLBACK_URL = os.environ.get('MPESA_CALLBACK_URL')
#     MPESA_API_URL = os.environ.get('MPESA_API_URL', 'https://sandbox.safaricom.co.ke')
    
#     # File Upload
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
#     UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


# class DevelopmentConfig(Config):
#     """Development configuration"""
#     DEBUG = True
#     TESTING = False


# class ProductionConfig(Config):
#     """Production configuration"""
#     DEBUG = False
#     TESTING = False


# class TestingConfig(Config):
#     """Testing configuration"""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig,
#     'testing': TestingConfig,
#     'default': DevelopmentConfig
# }
# import os
# from datetime import timedelta
# from dotenv import load_dotenv

# # Force load .env from the correct location
# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(os.path.dirname(basedir), '.env'))

# class Config:
#     """Base configuration"""
    
#     # Flask
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
#     # Database - FORCE PostgreSQL
#     DATABASE_URL = os.environ.get('DATABASE_URL')
#     if not DATABASE_URL or DATABASE_URL.startswith('sqlite'):
#         DATABASE_URL = 'postgresql://localhost/autoexpert_ke'
    
#     SQLALCHEMY_DATABASE_URI = DATABASE_URL
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ENGINE_OPTIONS = {
#         'pool_size': 10,
#         'pool_recycle': 3600,
#         'pool_pre_ping': True,
#         'max_overflow': 20,
#     }
    
#     # JWT
#     JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400)))
#     JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
#     JWT_TOKEN_LOCATION = ['headers']
#     JWT_HEADER_NAME = 'Authorization'
#     JWT_HEADER_TYPE = 'Bearer'
    
#     # CORS
#     FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5174')
    
#     # M-Pesa
#     MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT', 'sandbox')
#     MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
#     MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')
#     MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE')
#     MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY')
#     MPESA_CALLBACK_URL = os.environ.get('MPESA_CALLBACK_URL')
#     MPESA_API_URL = os.environ.get('MPESA_API_URL', 'https://sandbox.safaricom.co.ke')
    
#     # File Upload
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024
#     UPLOAD_FOLDER = os.path.join(os.path.dirname(basedir), 'uploads')
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


# class DevelopmentConfig(Config):
#     DEBUG = True
#     TESTING = False


# class ProductionConfig(Config):
#     DEBUG = False
#     TESTING = False


# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig,
#     'testing': TestingConfig,
#     'default': DevelopmentConfig
# }
import os
from datetime import timedelta
from dotenv import load_dotenv

# Force load .env from the correct location
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env'))

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database - FORCE PostgreSQL
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL or DATABASE_URL.startswith('sqlite'):
        DATABASE_URL = 'postgresql://localhost/autoexpert_ke'
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20,
    }
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # CORS
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5174')
    
    # M-Pesa
    MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT', 'sandbox')
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')
    MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE')
    MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY')
    MPESA_CALLBACK_URL = os.environ.get('MPESA_CALLBACK_URL')
    MPESA_API_URL = os.environ.get('MPESA_API_URL', 'https://sandbox.safaricom.co.ke')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.path.dirname(basedir), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}