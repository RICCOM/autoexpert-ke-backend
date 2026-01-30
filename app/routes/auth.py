# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from app import db
# from app.models.user import User
# from datetime import timedelta

# bp = Blueprint('auth', __name__)

# @bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
    
#     # Validation
#     required_fields = ['email', 'phone', 'password', 'first_name', 'last_name', 'role']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Missing required fields'}), 400
    
#     # Check if user exists
#     if User.query.filter_by(email=data['email']).first():
#         return jsonify({'error': 'Email already registered'}), 400
    
#     if User.query.filter_by(phone=data['phone']).first():
#         return jsonify({'error': 'Phone number already registered'}), 400
    
#     # Create user
#     user = User(
#         email=data['email'],
#         phone=data['phone'],
#         first_name=data['first_name'],
#         last_name=data['last_name'],
#         role=data['role']
#     )
#     user.set_password(data['password'])
    
#     db.session.add(user)
#     db.session.commit()
    
#     # Create access token
#     access_token = create_access_token(
#         identity=user.id,
#         expires_delta=timedelta(hours=24)
#     )
    
#     return jsonify({
#         'message': 'User registered successfully',
#         'access_token': access_token,
#         'user': user.to_dict()
#     }), 201

# @bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
    
#     if not data.get('email') or not data.get('password'):
#         return jsonify({'error': 'Email and password required'}), 400
    
#     user = User.query.filter_by(email=data['email']).first()
    
#     if not user or not user.check_password(data['password']):
#         return jsonify({'error': 'Invalid credentials'}), 401
    
#     if not user.is_active:
#         return jsonify({'error': 'Account is deactivated'}), 403
    
#     access_token = create_access_token(
#         identity=user.id,
#         expires_delta=timedelta(hours=24)
#     )
    
#     return jsonify({
#         'access_token': access_token,
#         'user': user.to_dict()
#     }), 200

# @bp.route('/me', methods=['GET'])
# @jwt_required()
# def get_current_user():
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)
    
#     if not user:
#         return jsonify({'error': 'User not found'}), 404
    
#     return jsonify(user.to_dict()), 200

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity
)
from app import db
from app.models.user import User, MechanicProfile
from datetime import timedelta

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    """Register a new user"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'phone', 'password', 'first_name', 'last_name', 'role']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate role
        if data['role'] not in ['customer', 'mechanic']:
            return jsonify({'error': 'Invalid role. Must be customer or mechanic'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.query.filter_by(phone=data['phone']).first():
            return jsonify({'error': 'Phone number already registered'}), 400
        
        # Validate password strength
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Create new user
        user = User(
            email=data['email'].lower().strip(),
            phone=data['phone'].strip(),
            first_name=data['first_name'].strip(),
            last_name=data['last_name'].strip(),
            role=data['role']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()
        
        # Create mechanic profile if role is mechanic
        if data['role'] == 'mechanic':
            mechanic_profile = MechanicProfile(
                user_id=user.id,
                specialization=data.get('specialization', ''),
                years_experience=data.get('years_experience', 0),
                bio=data.get('bio', '')
            )
            db.session.add(mechanic_profile)
        
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(include_profile=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """Login user"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=data['email'].lower().strip()).first()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if account is active
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated. Please contact support.'}), 403
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(include_profile=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/me', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict(include_profile=True)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/logout', methods=['POST', 'OPTIONS'])
@jwt_required()
def logout():
    """Logout user"""
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({'message': 'Logout successful'}), 200