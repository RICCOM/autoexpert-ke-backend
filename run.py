# #!/usr/bin/env python
# """
# AutoExpert KE Backend Application
# Main entry point for the Flask application
# """

# import os
# from app import create_app, db, socketio
# from app.models import (
#     user, mechanicProfile, service, booking,
#     chatRoom, message, payment, review
# )

# # Create application instance
# app = create_app(os.environ.get('FLASK_ENV', 'development'))


# @app.shell_context_processor
# def make_shell_context():
#     """Make database models available in Flask shell"""
#     return {
#         'db': db,
#         'User': user,
#         'MechanicProfile': mechanicProfiles,
#         'Service': service,
#         'Booking': booking,
#         'ChatRoom': chatRoom,
#         'Message': message,
#         'Payment': payment,
#         'Review': review,
#     }


# @app.cli.command()
# def init_db():
#     """Initialize the database with sample data"""
#     from app.utils.seed_data import seed_database
    
#     print("Creating database tables...")
#     db.create_all()
    
#     print("Seeding database with sample data...")
#     seed_database()
    
#     print("Database initialized successfully!")


# @app.cli.command()
# def create_admin():
#     """Create an admin user"""
#     from getpass import getpass
    
#     email = input("Admin email: ")
#     password = getpass("Admin password: ")
#     first_name = input("First name: ")
#     last_name = input("Last name: ")
#     phone = input("Phone number: ")
    
#     admin = User(
#         email=email,
#         first_name=first_name,
#         last_name=last_name,
#         phone=phone,
#         role='admin',
#         is_verified=True
#     )
#     admin.set_password(password)
    
#     db.session.add(admin)
#     db.session.commit()
    
#     print(f"Admin user created: {email}")


# if __name__ == '__main__':
#     # Run with SocketIO support
#     socketio.run(
#         app,
#         debug=app.config['DEBUG'],
#         host='0.0.0.0',
#         port=5000
#     )
#!/usr/bin/env python
"""
AutoExpert KE Backend Application
Main entry point for the Flask application
"""

import os
from app import create_app, db, socketio
from app.models import (
    User, MechanicProfile, Service, Booking,
    ChatRoom, Message, Payment, Review
)

# Create application instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'MechanicProfile': MechanicProfile,
        'Service': Service,
        'Booking': Booking,
        'ChatRoom': ChatRoom,
        'Message': Message,
        'Payment': Payment,
        'Review': Review,
    }


@app.cli.command()
def init_db():
    """Initialize the database with sample data"""
    from app.utils.seed_data import seed_database
    
    print("Creating database tables...")
    db.create_all()
    
    print("Seeding database with sample data...")
    seed_database()
    
    print("Database initialized successfully!")


@app.cli.command()
def create_admin():
    """Create an admin user"""
    from getpass import getpass
    
    email = input("Admin email: ")
    password = getpass("Admin password: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone = input("Phone number: ")
    
    admin = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        role='admin',
        is_verified=True
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Admin user created: {email}")


if __name__ == '__main__':
    # Run with SocketIO support
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )