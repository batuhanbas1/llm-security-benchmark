def delete_user(user_id):
    import sqlite3
    conn = sqlite3.connect("users.db")
    query = f"DELETE FROM users WHERE id = {user_id}"
    conn.execute(query)