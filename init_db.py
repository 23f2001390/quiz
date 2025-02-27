from datetime import datetime
from app import create_app, db
from models.user import User
from models.quiz import Subject, Chapter, Quiz, Question
from models.score import Score

def init_db():
    app = create_app()
    with app.app_context():
        # Drop all tables and create them again
        db.drop_all()
        db.create_all()
        db.session.commit()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@quizmaster.com').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@quizmaster.com',
                full_name='Admin User',
                is_admin=True,
                date_of_birth=datetime.strptime('2000-01-01', '%Y-%m-%d')
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Admin user created successfully!')
        else:
            print('Admin user already exists.')

if __name__ == '__main__':
    init_db() 