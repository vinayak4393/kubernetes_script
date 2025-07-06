# init_db.py
import os
from app import app, db, User # Import app, db, and User model from your app.py
from werkzeug.security import generate_password_hash

# This script runs within the Flask application context
# to ensure SQLAlchemy and database connection are properly set up.
with app.app_context():
    print("Attempting to create database tables...")
    db.create_all()
    print("Database tables creation attempt complete.")

    # Optional: Create a default admin user if none exists
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', email='admin@example.com', role='admin')
        admin_user.set_password(os.environ.get('DEFAULT_ADMIN_PASSWORD', 'adminpass')) # Get password from env
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created.")
    else:
        print("Admin user already exists.")

    # Optional: Create a default instructor user if none exists
    if not User.query.filter_by(username='instructor1').first():
        instructor_user = User(username='instructor1', email='instructor1@example.com', role='instructor')
        instructor_user.set_password(os.environ.get('DEFAULT_INSTRUCTOR_PASSWORD', 'instructorpass')) # Get password from env
        db.session.add(instructor_user)
        db.session.commit()
        print("Default instructor user created.")
    else:
        print("Instructor user already exists.")

    print("Database initialization script finished.")

