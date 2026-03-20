CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    interest VARCHAR(80) DEFAULT 'Technology',
    visits INTEGER DEFAULT 0,
    profile_pic VARCHAR(200) DEFAULT 'default_user.png'
);
