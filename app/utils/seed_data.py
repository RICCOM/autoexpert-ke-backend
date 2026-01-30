from app import db
from app.models.user import User, MechanicProfile
from app.models.service import Service
from app.models.booking import Booking
from app.models.chat import ChatRoom
from datetime import datetime, timedelta


def seed_database():
    """Seed database with sample data"""
    
    print("Creating sample users...")
    
    # Create customers
    customer1 = User(
        email='customer1@example.com',
        phone='0712345678',
        first_name='John',
        last_name='Doe',
        role='customer',
        is_verified=True
    )
    customer1.set_password('password123')
    
    customer2 = User(
        email='customer2@example.com',
        phone='0723456789',
        first_name='Jane',
        last_name='Smith',
        role='customer',
        is_verified=True
    )
    customer2.set_password('password123')
    
    # Create mechanics
    mechanic1 = User(
        email='mechanic1@example.com',
        phone='0734567890',
        first_name='Mike',
        last_name='Johnson',
        role='mechanic',
        is_verified=True
    )
    mechanic1.set_password('password123')
    
    mechanic2 = User(
        email='mechanic2@example.com',
        phone='0745678901',
        first_name='Sarah',
        last_name='Williams',
        role='mechanic',
        is_verified=True
    )
    mechanic2.set_password('password123')
    
    # Create admin
    admin = User(
        email='admin@autoexpert.ke',
        phone='0756789012',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_verified=True
    )
    admin.set_password('admin123')
    
    db.session.add_all([customer1, customer2, mechanic1, mechanic2, admin])
    db.session.commit()
    
    print("Creating mechanic profiles...")
    
    # Create mechanic profiles
    profile1 = MechanicProfile(
        user_id=mechanic1.id,
        specialization='Engine Diagnostics',
        years_experience=5,
        certification='ASE Certified',
        bio='Experienced mechanic specializing in engine repairs and diagnostics.',
        hourly_rate=800,
        rating=4.8,
        total_reviews=15,
        total_jobs=50
    )
    
    profile2 = MechanicProfile(
        user_id=mechanic2.id,
        specialization='Brake Systems',
        years_experience=3,
        certification='Toyota Certified',
        bio='Expert in brake systems and general maintenance.',
        hourly_rate=600,
        rating=4.9,
        total_reviews=20,
        total_jobs=75
    )
    
    db.session.add_all([profile1, profile2])
    db.session.commit()
    
    print("Creating services...")
    
    # Create services
    services = [
        Service(
            name='Engine Diagnostics',
            description='Complete engine diagnosis and troubleshooting',
            base_price=500,
            icon='wrench',
            category='Engine',
            estimated_duration=60
        ),
        Service(
            name='Brake System Check',
            description='Full brake inspection and repair',
            base_price=400,
            icon='shield',
            category='Brakes',
            estimated_duration=45
        ),
        Service(
            name='General Consultation',
            description='Expert advice on any car issues',
            base_price=300,
            icon='clock',
            category='Consultation',
            estimated_duration=30
        ),
        Service(
            name='Emergency Support',
            description='24/7 emergency roadside assistance',
            base_price=800,
            icon='phone',
            category='Emergency',
            estimated_duration=120
        ),
        Service(
            name='Oil Change',
            description='Complete oil and filter change service',
            base_price=350,
            icon='droplet',
            category='Maintenance',
            estimated_duration=30
        ),
    ]
    
    db.session.add_all(services)
    db.session.commit()
    
    print("Creating sample bookings...")
    
    # Create sample bookings
    booking1 = Booking(
        customer_id=customer1.id,
        mechanic_id=mechanic1.id,
        service_id=services[0].id,
        status='completed',
        description='Car engine making strange noises',
        vehicle_info={'make': 'Toyota', 'model': 'Corolla', 'year': '2018'},
        price=services[0].base_price,
        payment_status='paid',
        completed_at=datetime.utcnow() - timedelta(days=2)
    )
    
    booking2 = Booking(
        customer_id=customer1.id,
        service_id=services[1].id,
        status='pending',
        description='Brakes squeaking when stopping',
        vehicle_info={'make': 'Honda', 'model': 'Civic', 'year': '2020'},
        price=services[1].base_price
    )
    
    db.session.add_all([booking1, booking2])
    db.session.commit()
    
    print("Creating chat rooms...")
    
    # Create chat rooms
    for booking in [booking1, booking2]:
        chat_room = ChatRoom(booking_id=booking.id)
        db.session.add(chat_room)
    
    db.session.commit()
    
    print("✅ Database seeded successfully!")
    print("\nSample Users:")
    print("Customer 1: customer1@example.com / password123")
    print("Customer 2: customer2@example.com / password123")
    print("Mechanic 1: mechanic1@example.com / password123")
    print("Mechanic 2: mechanic2@example.com / password123")
    print("Admin: admin@autoexpert.ke / admin123")
