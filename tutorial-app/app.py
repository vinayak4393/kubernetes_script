import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# --- Flask Application Setup ---
app = Flask(__name__)

# Configuration
# Use environment variables for sensitive data and dynamic configuration in Kubernetes
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_very_secret_key_for_dev')
# Database URI: Connect to the PostgreSQL database service in Kubernetes
# Format: postgresql://user:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://mysecretuser:mypassword@database-service:5432/mydatabase'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to login page if not authenticated

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # FIX: Increased password_hash length to accommodate longer hashes
    password_hash = db.Column(db.String(256), nullable=False)
    # Role management: 'student', 'instructor', 'admin'
    role = db.Column(db.String(20), default='student', nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instructor = db.relationship('User', backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f'<Course {self.title}>'

# --- Flask-Login User Loader ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---

@app.route('/')
def welcome():
    """Welcome page."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        # Check if username or email already exists
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or Email already exists!', 'warning')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('welcome'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    return render_template('dashboard.html', user=current_user)

@app.route('/courses')
def courses():
    """Display all available courses."""
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    """Add a new course (requires instructor/admin role)."""
    # Simple role check: Only instructors or admins can add courses
    if current_user.role not in ['instructor', 'admin']:
        flash('You do not have permission to add courses.', 'danger')
        return redirect(url_for('courses'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title:
            flash('Course title is required!', 'danger')
            return redirect(url_for('add_course'))

        new_course = Course(title=title, description=description, instructor_id=current_user.id)
        db.session.add(new_course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses'))
    return render_template('add_course.html')

@app.route('/contact')
def contact():
    """Contact Us page."""
    return render_template('contact.html')

# --- Main execution ---
if __name__ == '__main__':
    # When running locally:
    # Set FLASK_SECRET_KEY and DATABASE_URL in your environment or directly here for testing.
    # For local testing with SQLite:
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    # db.create_all() # For local SQLite, you can call create_all here
    app.run(debug=False, host='0.0.0.0', port=5000) # In K8s, debug should be False

