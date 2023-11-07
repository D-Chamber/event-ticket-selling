from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Initialize an empty user data dictionary
user_data = {}

# Initialize an empty ticket/event data dictionary
event_data = {}


# Load user data from a JSON file on server startup
def load_user_data():
    global user_data
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}


# Load ticket/event data from a JSON file on server startup
def load_events_data():
    global event_data
    try:
        with open('events.json', 'r') as file:
            event_data = json.load(file)
    except FileNotFoundError:
        event_data = {}


# Save user data to a JSON file
def save_user_data():
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file)


# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username in user_data:
        return jsonify({"message": "Username already exists"}), 400
    user_data[username] = {"password": password, "points": 1000}
    save_user_data()  # Save the updated user data to the file
    return jsonify({"message": "Registration successful"}), 201


# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username not in user_data or user_data[username]["password"] != password:
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({"message": "Login successful", "points": user_data[username]["points"]})


# Add points to a user's account
@app.route('/add_points', methods=['POST'])
def add_points():
    data = request.get_json()
    username = data.get("username")
    points = data.get("points")
    if username not in user_data:
        return jsonify({"message": "User not found"}), 404
    user_data[username]["points"] += points
    save_user_data()  # Save the updated user data to the file
    return jsonify({"message": "Points added successfully", "points": user_data[username]["points"]})


if __name__ == '__main__':
    load_user_data()  # Load user data from the JSON file on server startup
    app.run(debug=True)
