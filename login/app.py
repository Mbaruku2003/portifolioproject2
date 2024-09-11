# app.py
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# Route for login page
@app.route('/')
def home():
    return render_template('login.html')

# Route to handle login logic
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if user exists
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        flash('Login successful!')
        return redirect(url_for('dashboard'))  # Redirect to another page after login
    else:
        flash('Invalid credentials!')
        return redirect(url_for('home'))

# Dashboard page after login
@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard!"

# Register a new user (This would be your registration route)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='sha256')

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('home'))

    return render_template('registration.html')

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
