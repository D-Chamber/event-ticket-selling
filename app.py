from flask import Flask, request, jsonify
from loguru import logger
import json

# Ticket purchasing server V.1.0
# Written by Tim Nguyen and Andrew Gonye
app = Flask(__name__)

# Initialization of the user_data list
user_data = []

# Initialization of the event_data list
event_data = []


# Load user data from a JSON file on server startup
def load_user_data():
    # Grabs the global variable of user_data to be used within this function
    global user_data
    # Uses try-except to check if the file exists, if it does, it opens it and loads the data into user_data
    try:
        # opens the file in read mode and extends the initial list with the json data
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
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
    # Grabs the global variable of event_data to be used within this function
    global event_data
    try:
        # opens the file in read mode and sets the initial list with the json data
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
    # Uses request module to get the json data from the client when the client posts it to the server endpoint
    data = request.get_json()
    # Parse the json data to get the username and password
    username = data.get("username")
    password = data.get("password")
    # Checks if the username already exists in the user_data list
    for user in user_data:
        if user["username"] == username:
            return jsonify({"message": "Username already exists"}), 400

    # If the username doesn't exist, it appends the username and password to the user_data list
    user_data.append({"username": username, "password": password, "points": 1000, "admin": False,
                      "tickets": [{"event_name": "League of Legends World Cup", "quantity": 0},
                                  {"event_name": "Overwatch League", "quantity": 0}]})

    # Saves the user_data to the json file
    save_user_data()
    return jsonify({"message": "Registration successful"}), 201


# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    # Uses request module to get the json data from the client when the client posts it to the server endpoint
    data = request.get_json()
    # Parse the json data to get the username and password
    username = data.get("username")
    password = data.get("password")
    # Checks if the username and password match the user in the user_data list
    for user in user_data:
        if user["username"] == username and user["password"] == password:
            # If the account has the admin flag, it returns the admin flag as true
            if user["admin"]:
                return jsonify({"message": "Login successful", "points": user["points"], "admin": True}), 200
            return jsonify({"message": "Login successful", "points": user["points"], "admin": False}), 200
    return jsonify({"message": "Invalid username or password"}), 401


# Buy tickets endpoint
@app.route('/buy_tickets', methods=['POST'])
def buy_ticket():
    # Uses request module to get the json data from the client when the client posts it to the server endpoint
    data = request.get_json()
    # Parse the json data to get the username, event ID, and number of tickets
    username = data.get("username")
    event_id = data.get("id")
    number_of_tickets = data.get("quantity")

    # Checks if the user has enough points to purchase the tickets by grabbing a reference to the user itself and
    # setting it to temp user
    temp_user_info = {}
    for user in user_data:
        if user["username"] == username:
            temp_user_info = user
    available_points = temp_user_info["points"]

    # Grabs the event data and sets it to temp event data and using that reference to see if the ticket's available are
    # greater than 0, if it is, it subtracts the points from the user and updates the event data
    temp_event_data = {}
    for event in event_data:
        if event["id"] == event_id:
            temp_event_data = event
    if temp_event_data["tickets_available"] != 0:
        available_points -= (temp_event_data["tickets_price"] * number_of_tickets)
        temp_event_data["tickets_available"] -= number_of_tickets
        update_events_data()

    # checks event ID and updates the path of ticket being purchased accordingly
    temp_user_info["points"] = available_points
    if event_id == 1:
        temp_user_info["tickets"][0] = ({"event_name": temp_event_data["event_name"],
                                         "quantity": temp_user_info["tickets"][0]["quantity"] + number_of_tickets})
        save_user_data()
    elif event_id == 2:
        temp_user_info["tickets"][1] = ({"event_name": temp_event_data["event_name"],
                                         "quantity": temp_user_info["tickets"][1]["quantity"] + number_of_tickets})
        save_user_data()

    return jsonify({"message": f"successfully bought {number_of_tickets} tickets", "points": temp_user_info["points"]})


# Check available tickets endpoint
@app.route('/check_available_tickets', methods=['GET'])
def check_available_tickets():
    return jsonify(event_data), 200


# Check owned tickets endpoint
@app.route('/check_owned_tickets', methods=['POST'])
def check_owned_tickets():
    data = request.get_json()
    username = data.get("username")
    temp_user = {}
    for user in user_data:
        if user["username"] == username:
            temp_user = user

    return jsonify({"Tickets": temp_user["tickets"]}), 200


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


def main():
    load_user_data()
    load_events_data()


main()


if __name__ == '__main__':
    main()
    app.run(debug=True)
