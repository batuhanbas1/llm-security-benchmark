import sqlite3

def add_user(username):
    with sqlite3.connect("users.db") as conn:
        conn.execute("INSERT INTO users (username) VALUES (?)", (username,))