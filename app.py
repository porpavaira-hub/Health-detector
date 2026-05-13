from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# DATABASE
conn = sqlite3.connect('health.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    name TEXT,
    age TEXT,
    gender TEXT,
    height TEXT,
    weight TEXT,
    disease TEXT
)
''')

conn.commit()

# HOME
@app.route('/')
def home():
    return "Health Detector Backend Running"

# LOGIN / SIGNUP
@app.route('/login', methods=['POST'])
def login():

    data = request.json

    username = data['username']
    password = data['password']

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    # LOGIN
    if user:

        if user[2] == password:
            return jsonify({
                "message":"Login Successful",
                "status":"success"
            })

        else:
            return jsonify({
                "message":"Wrong Password",
                "status":"error"
            })

    # AUTO SIGNUP
    else:

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )

        conn.commit()

        return jsonify({
            "message":"Account Created",
            "status":"success"
        })

# SAVE HEALTH DETAILS
@app.route('/save-details', methods=['POST'])
def save_details():

    data = request.json

    cursor.execute('''
    UPDATE users
    SET name=?,
        age=?,
        gender=?,
        height=?,
        weight=?,
        disease=?
    WHERE username=?
    ''', (
        data['name'],
        data['age'],
        data['gender'],
        data['height'],
        data['weight'],
        data['disease'],
        data['username']
    ))

    conn.commit()

    return jsonify({
        "message":"Details Saved Successfully"
    })

# ADMIN DASHBOARD
@app.route('/admin', methods=['GET'])
def admin():

    password = request.args.get("password")

    if password != "admin":
        return jsonify({
            "message":"Wrong Admin Password"
        })

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    all_users = []

    for user in users:

        all_users.append({
            "id":user[0],
            "username":user[1],
            "name":user[3],
            "age":user[4],
            "gender":user[5],
            "height":user[6],
            "weight":user[7],
            "disease":user[8]
        })

    return jsonify(all_users)

# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)
