# Secure Programmatic Advertising Demo (Flask + HTTPS)

A secure programmatic advertising demo using Flask and HTTPS. This project focuses on implementing robust web security practices, including **HTTPS (SSL/TLS)**, **Signed Cookies**, and persistent **Session Tracking**.

## 🚀 Features
- **Local HTTPS**: Uses `mkcert` for a trusted local development environment.
- **Secure Sessions**: Implements Flask `session` for tamper-proof visitor counting.
- **User Profiles**: Persistent storage of user interests and visit analytics.
- **Targeted Ads**: Basic ad targeting logic based on user data and loyalty.
- **Database Persistence**: SQLite-backed user management with hashed passwords and profile tracking.

---

## 🛡️ Security Features Explained
- **Secure=True**: Ensures cookies are only sent over encrypted HTTPS connections.
- **HttpOnly=True**: Prevents client-side scripts (JavaScript) from accessing session cookies, mitigating XSS attacks.
- **SameSite=Lax**: Protects against Cross-Site Request Forgery (CSRF) while allowing essential functionality.
- **Session Signing**: Uses a `SECRET_KEY` to sign data, preventing users from manually editing their visit counts in the browser console.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
You'll need `mkcert` to handle local SSL certificates.
- **Windows**: `choco install mkcert`
- **macOS**: `brew install mkcert`
- **Linux (Ubuntu)**: `sudo apt install mkcert libnss3-tools`

Run the initial setup:
```bash
mkcert -install
```

### 2. Generate Local Certificates
```bash
mkcert localhost 127.0.0.1 ::1
```
*Creates `localhost+2.pem` and `localhost+2-key.pem` files.*

### 3. Installation
```bash
pip install -r requirements.txt
```

### 4. Database Setup
The application uses SQLite. To manually initialize the schema using `schema.sql`:
```bash
sqlite3 users.db < schema.sql
```
*(Note: The app will also initialize the database automatically on startup if `users.db` is missing.)*

### 5. Run the Application
```bash
python cookies.py
```
*Access the secure portal at:* **`https://127.0.0.1:5001`**

---

## 📂 Project Structure
- `cookies.py`: Main Flask application and database models.
- `schema.sql`: Database table definitions for SQLite.
- `users.db`: Persistent database file (ignored by Git).
- `requirements.txt`: Python package dependencies.
- `.gitignore`: Prevents sensitive certificates and local databases from being committed.
