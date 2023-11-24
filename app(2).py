from flask import Flask, request, jsonify
from loguru import logger
import json

# Ticket purchasing server V.1.0
# Written by Tim Nguyen and Andrew Gonye
app = Flask(__name__)

user_data = [

]

event_data = []


# Load user data from a JSON file on server startup
def load_user_data():
    global user_data
    try:
        with open('user_data.json', 'r') as file:
            user_data.extend(json.load(file))
    except FileNotFoundError:
        logger.error("File not found")


# Saves the user_data by opening the file and dumping the user_data into it
def save_user_data():
    try:
        with open('user_data.json', 'w') as file:
            json.dump(user_data, file)
    except FileNotFoundError:
        logger.error("File not found")


# Load ticket/event data from a JSON file on server startup
def load_events_data():
    global event_data
    try:
        with open('events.json', 'r') as file:
            event_data = json.load(file)
    except FileNotFoundError:
        logger.error("File not found")

# Function to update the event data json
def update_events_data():
    try:
        with open('events.json', 'w') as file:
            json.dump(event_data, file)
    except FileNotFoundError:
        logger.error("File not found")


# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    for user in user_data:
        if user["username"] == username:
            return jsonify({"message": "Username already exists"}), 400
    user_data.append({"username": username, "password": password, "points": 1000, "admin": False, "tickets": [{"event_name": "League of Legends World Cup", "quantity": 0},{"event_name": "Overwatch League", "quantity": 0}]})

    save_user_data()
    return jsonify({"message": "Registration successful"}), 201


# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    for user in user_data:
        if user["username"] == username and user["password"] == password:
            if user["admin"]:
                return jsonify({"message": "Login successful", "points": user["points"], "admin": True}), 200
            return jsonify({"message": "Login successful", "points": user["points"]}), 200
    return jsonify({"message": "Invalid username or password"}), 401


# Buy tickets endpoint
@app.route('/buy_tickets', methods=['POST'])
def buy_ticket():
    data = request.get_json()
    username = data.get("username")
    event_id = data.get("id")
    number_of_tickets = data.get("quantity")
    temp_user_info = {}
    for user in user_data:
        if user["username"] == username:
            temp_user_info = user
    available_points = temp_user_info["points"]

    temp_event_data = {}
    for event in event_data:
        if event["id"] == event_id:
            temp_event_data = event
    if temp_event_data["tickets_available"] != 0:
        if available_points - (temp_event_data["tickets_price"]*number_of_tickets) >= 0:
            available_points -= (temp_event_data["tickets_price"] * number_of_tickets)
            temp_event_data["tickets_available"] -= number_of_tickets
            update_events_data()
        else:
            return jsonify({"message": f"You do not have enough points to purchase these tickets."})
    #checks event ID and updates the path of ticket being purchased accordingly
    temp_user_info["points"] = available_points
    if event_id == 1:
        temp_user_info["tickets"][0] = ({"event_name": temp_event_data["event_name"], "quantity": temp_user_info["tickets"][0]["quantity"] + number_of_tickets})
        save_user_data()
        return jsonify({"message": f"successfully bought {number_of_tickets} tickets", "points": temp_user_info["points"]})
    elif event_id == 2:
        temp_user_info["tickets"][1] = ({"event_name": temp_event_data["event_name"], "quantity": temp_user_info["tickets"][1]["quantity"] + number_of_tickets})
        save_user_data()
        return jsonify({"message": f"successfully bought {number_of_tickets} tickets", "points": temp_user_info["points"]})
    else:
        return jsonify({"message": f"Purchase Unsuccessful"})


# Check available tickets endpoint
@app.route('/check_available_tickets', methods=['GET'])
def check_available_tickets():
    return jsonify({"message": f"Current ticket information:", "event1": event_data[0], "event2": event_data[1]}), 200


#Check owned tickets endpoint
@app.route('/check_owned_tickets', methods=['POST'])
def check_owned_tickets():
    data= request.get_json()
    username=data.get("username")
    temp_user = {}
    for user in user_data:
        if user["username"] == username:
            temp_user = user

    #return jsonify({"Tickets":temp_user["tickets"]}), 200
    return jsonify({"message": f"Current tickets for {username}:", "Tickets1": temp_user["tickets"][0],"Tickets2": temp_user["tickets"][1]}), 200


# Add points endpoint
@app.route('/add_points', methods=['POST'])
def add_points():
    data = request.get_json()
    username = data.get("username")
    points = data.get("points")
    for user in user_data:
        if user["username"] == username:
            user["points"] += points
            save_user_data()
            return jsonify({"message": "Points added successfully", "points": user["points"]}), 200
    return jsonify({"message": "Invalid username or password"}), 401


if __name__ == '__main__':
    load_user_data()
    load_events_data()
    app.run(debug=True)
