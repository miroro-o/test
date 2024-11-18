import sqlite3

def init_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            status TEXT
        )
    ''')
    connection.commit()
    connection.close()

def add_user(user_id, username, first_name, last_name, status):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, status))
    connection.commit()
    connection.close()

def get_user(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    connection.close()
    return user

def update_user_status(user_id, status):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET status = ? WHERE user_id = ?', (status, user_id))
    connection.commit()
    connection.close()