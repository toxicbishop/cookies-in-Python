# Secure Programmatic Advertising Demo (Flask + HTTPS)

This project demonstrates a basic programmatic advertising engine built with Flask. It focuses on implementing secure web practices, including **HTTPS (SSL/TLS)**, **Signed Cookies**, and **Session Tracking** to prevent data tampering.

## 🚀 Features
- **Local HTTPS**: Uses `mkcert` for a trusted local development environment.
- **Secure Sessions**: Implements Flask `session` for tamper-proof visit counting.
- **Targeted Logic**: Simulates basic ad targeting based on user interest and loyalty (visit count).
- **Cookie Management**: Includes routes to view, set, and clear secure cookies.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
You will need `mkcert` to handle the local SSL certificates.

- **Linux (Ubuntu):** `sudo apt install mkcert libnss3-tools`
- **macOS:** `brew install mkcert`
- **Windows:** `choco install mkcert`

Run the initial setup:
```bash
mkcert -install
```
## Generate Certificates
``bash
mkcert localhost 127.0.0.1 ::1
```
## Installation
``bash
pip install -r requirements.txt
```

## Run app
``bash
python app.py
```

## 🛡️ Security Features Explained

    Secure=True: Ensures cookies are only sent over encrypted HTTPS connections.

    HttpOnly=True: Prevents client-side scripts (JavaScript) from accessing the cookies, mitigating XSS attacks.

    SameSite=Lax: Protects against Cross-Site Request Forgery (CSRF).

    Session Signing: Uses a SECRET_KEY to sign data, preventing users from manually editing their visit counts in the browser console.

## 📂 Project Structure

    app.ipynb: Main application logic.

    steps.txt: Quick-start guide for environment setup.

    requirements.txt: Python library dependencies.

    .gitignore: Prevents sensitive .pem files from being uploaded.
