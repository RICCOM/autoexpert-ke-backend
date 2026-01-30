from app import create_app, db
from app.utils.seed_data import seed_database

app = create_app()

with app.app_context():
    print('Creating database tables...')
    db.create_all()
    
    print('Seeding database with sample data...')
    seed_database()
    
    print('✅ Database initialized successfully!')