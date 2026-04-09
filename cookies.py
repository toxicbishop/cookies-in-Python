import os
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 1. Configurations
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-key-789')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload Settings
UPLOAD_FOLDER = 'static/profile_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)
)

db = SQLAlchemy(app)

# 2. Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    interest = db.Column(db.String(80), default='Technology')
    visits = db.Column(db.Integer, default=0)
    profile_pic = db.Column(db.String(200), default='default_user.png')

# 3. Enhanced HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure User Portal</title>
    <style>
        body { font-family: sans-serif; padding: 40px; background: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; }
        .profile-img { width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #3498db; }
        button { cursor: pointer; padding: 8px 15px; margin: 5px; }
    </style>
</head>
<body>
    <div class="card">
    <h1>Secure Ad Dashboard</h1>
    {% if user %}
        <div style="text-align: center;">
            <img src="/static/profile_pics/{{ user.profile_pic }}" class="profile-img" onerror="this.src='https://ui-avatars.com/api/?name={{ user.username }}'">
            <p>Welcome, <b>{{ user.username }}</b>! | <a href="/logout">Logout</a></p>
        </div>
        
        <form action="/upload_profile" method="post" enctype="multipart/form-data" style="margin-top: 10px;">
            <input type="file" name="pic" accept="image/*" required>
            <button type="submit">Update Photo</button>
        </form>

        <hr>
        <p>Interest Profile: <b style="color: #3498db;">{{ user.interest }}</b></p>
        <p>Total Secure Visits: <b>{{ user.visits }}</b></p>
        
        <h3>Change Interest:</h3>
        <a href='/set_interest/Gaming'><button>Gaming</button></a>
        <a href='/set_interest/Cooking'><button>Cooking</button></a>
        <a href='/set_interest/Technology'><button>Technology</button></a>
    {% else %}
        <h3>Login or Create Account</h3>
        <form action="/auth" method="post">
            <input type="text" name="username" placeholder="Username" required style="display:block; margin: 10px 0; width: 90%;">
            <input type="password" name="password" placeholder="Password" required style="display:block; margin: 10px 0; width: 90%;">
            <button type="submit" name="action" value="login" style="background: #3498db; color: white; border: none;">Login</button>
            <button type="submit" name="action" value="register">Register</button>
        </form>
    {% endif %}
    <hr>
    <p><a href='/show_ad'> View JSON Ad Engine</a> | <a href='/clear'>Reset Session</a></p>
    </div>
</body>
</html>
"""

# 4. Routes
@app.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            user.visits += 1
            db.session.commit()
    return render_template_string(HTML_TEMPLATE, user=user)

@app.route('/auth', methods=['POST'])
def auth():
    username, password, action = request.form.get('username'), request.form.get('password'), request.form.get('action')
    if action == 'register':
        if User.query.filter_by(username=username).first(): return "User exists!", 400
        db.session.add(User(username=username, password_hash=generate_password_hash(password)))
        db.session.commit()
        return "Registered! Please go back and login."
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session.permanent = True
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return "Invalid Credentials", 401

@app.route('/upload_profile', methods=['POST'])
def upload_profile():
    if 'user_id' not in session: return redirect(url_for('index'))
    file = request.files.get('pic')
    if file and file.filename != '':
        filename = secure_filename(f"user_{session['user_id']}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = User.query.get(session['user_id'])
        user.profile_pic = filename
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/set_interest/<new_interest>')
def set_interest(new_interest):
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user.interest = new_interest
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/show_ad')
def show_ad():
    user = User.query.get(session.get('user_id'))
    interest = user.interest if user else "General"
    return jsonify({"ad": f"Special deal for {interest} lovers!", "visits": user.visits if user else 0})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    cert, key = 'localhost+2.pem', 'localhost+2-key.pem'
    if os.path.exists(cert):
        app.run(host='127.0.0.1', port=5001, ssl_context=(cert, key), debug=True)