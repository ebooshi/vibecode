from flask import Flask, request, jsonify
import uuid
from datetime import datetime
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# MySQL connection config — change these to your values
db_config = {
    'host': 'localhost',
    'user': 'root',         # your MySQL username
    'password': 'Atlantida563!', # your MySQL password
    'database': 'myappdb'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['GET'])
def home():
    return "hola cabron"

@app.route('/comedor', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing 'name' in request body"}), 400

    user_id = str(uuid.uuid4())
    name = data['name']
    created_at = datetime.utcnow()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO users (id, name, created_at) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, name, created_at))
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({
        "id": user_id,
        "name": name,
        "created_at": created_at.isoformat()
    }), 201

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
