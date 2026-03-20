import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response, session, redirect, url_for

app = Flask(__name__)

# Security: Secret key for signing sessions
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'secure-dev-key-123')

# HTTPS & Cookie Security Configuration
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7) # Cookie lasts 7 days
)

@app.route('/')
def index():
    # Make this specific user's session last beyond browser close
    session.permanent = True 
    
    # Update Stats
    count = session.get('visits', 0) + 1
    session['visits'] = count
    
    last_visit = session.get('last_visit', 'First time!')
    session['last_visit'] = datetime.now().strftime("%H:%M:%S")

    interest = session.get('interest', 'Technology')

    msg = f"""
    <html>
    <head><title>Secure Ad Dashboard</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1>Secure Ad Dashboard (Permanent)</h1>
        <p>Current Interest Profile: <b style="color: blue;">{interest}</b></p>
        <p>Session Visits: <b>{count}</b> | Last Seen: <b>{last_visit}</b></p>
        <hr>
        <h3>Change Interest Profile:</h3>
        <a href='/set_interest/Gaming'><button>Gaming</button></a>
        <a href='/set_interest/Cooking'><button>Cooking</button></a>
        <a href='/set_interest/Technology'><button>Technology</button></a>
        <hr>
        <p><a href='/show_ad'>🚀 View JSON Ad Engine</a> | <a href='/clear'>🧹 Reset All</a></p>
    </body>
    </html>
    """
    return msg

@app.route('/set_interest/<new_interest>')
def set_interest(new_interest):
    session.permanent = True
    allowed = ['Gaming', 'Cooking', 'Technology']
    if new_interest in allowed:
        session['interest'] = new_interest
    return redirect(url_for('index'))

@app.route('/show_ad')
def show_ad():
    interest = session.get('interest', 'General')
    visits = session.get('visits', 0)
    tier = "Premium" if visits > 5 else "Standard"
    
    ad_database = {
        "Technology": "Get the new M4 MacBook Pro today!",
        "Gaming": "Pre-order the latest RPG masterpiece now.",
        "Cooking": "Upgrade your kitchen with 20% off air fryers."
    }
    
    selected_ad = ad_database.get(interest, "Check out our daily deals!")
        
    return jsonify({
        "ad_content": f"[{tier}] {selected_ad}",
        "targeting_data": {
            "profile": interest,
            "visit_history": visits,
            "last_active": session.get('last_visit')
        },
        "connection": "SSL/TLS Verified"
    })

@app.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    cert_file = 'localhost+2.pem'
    key_file = 'localhost+2-key.pem'
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"\n--- 🔒 Secure Permanent Server Started at https://127.0.0.1:5001 ---")
        app.run(host='127.0.0.1', port=5001, ssl_context=(cert_file, key_file), debug=True)
    else:
        print("\n--- ❌ ERROR: SSL Certificates Not Found! ---")