from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

app = create_app()

with app.app_context():
    # Create all database tables
    db.create_all()
    
    # Create a test user if none exists
    if not User.query.first():
        test_user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        test_user.hash_password('test123')
        db.session.add(test_user)
        db.session.commit()
        print('Created test user: test@example.com / test123')
    
    print('Database initialized successfully!') 