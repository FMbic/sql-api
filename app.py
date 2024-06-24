from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE)''')
        conn.commit()

init_db()

@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                       (new_user['name'], new_user['email']))
        conn.commit()
        return jsonify({'id': cursor.lastrowid}), 201

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    updates = request.json
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        if 'name' in updates:
            cursor.execute("UPDATE users SET name = ? WHERE id = ?", 
                           (updates['name'], user_id))
        if 'email' in updates:
            cursor.execute("UPDATE users SET email = ? WHERE id = ?", 
                           (updates['email'], user_id))
        conn.commit()
        return jsonify({'msg': 'User updated'}), 200
    
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return jsonify({'msg': 'User deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
