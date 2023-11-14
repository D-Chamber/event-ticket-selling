import requests

# Ticket purchasing client V.1.0
# Written by Tim Nguyen and Andrew Gonye
# Server URL
SERVER_URL = 'http://127.0.0.1:5000'  # Change to your server's URL

# setting username and admin for later global usage
username = ""
admin = False


# setup of user registration, user passes username and password and posts it server-side
def register_user(username, password):
    data = {"username": username, "password": password}
    response = requests.post(f'{SERVER_URL}/register', json=data)
    return response.json()


# setup of user login, user passes username and password and posts it server-side
def login_user(username, password):
    data = {"username": username, "password": password}
    response = requests.post(f'{SERVER_URL}/login', json=data)
    return response.json()


# get call for available tickets
def check_available_tickets():
    data = requests.get(f"{SERVER_URL}/check_available_tickets")
    return data.json()


# post call for checking user's owned tickets
def check_owned_tickets():
    data = {"username": username}
    response = requests.post(f"{SERVER_URL}/check_owned_tickets", json=data)
    return response.json()


# post call for purchasing tickets
def buy_tickets(event, quantity):
    data = {"username": username, "id": event, "quantity": quantity}
    response = requests.post(f'{SERVER_URL}/buy_tickets', json=data)
    return response.json()


# post call for adding points (ADMIN ONLY)
def add_points(points):
    data = {"username": username, "points": points}
    response = requests.post(f"{SERVER_URL}/add_points", json=data)
    return response.json()


def main():
    # instantiating globals
    global username
    global admin
    logged_in = False
    # main runner for login and register until logged in
    while True:
        if not logged_in:
            print("1. Register")
            print("2. Login")
        else:
            print("3. Check Available Tickets")
            print("4. Check Owned Tickets")
            print("5. Buy Tickets")
            if admin:
                print("6. Add Points")
            print("7. Logout")

        print("8. Exit")
        choice = input("Enter your choice: ")
        # calls register function
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            result = register_user(username, password)
            print(result["message"])
        # calls login function
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            result = login_user(username, password)
            if "message" in result:
                print(result["message"])
                if "points" in result:
                    print(f"Points: {result['points']}")
                    logged_in = True
                if "admin" in result:
                    admin = result["admin"]
            else:
                logged_in = False
        # calls available tickets function
        elif choice == '3' and logged_in:
            print(check_available_tickets())
            # Implement code to display available tickets
        # calls owned tickets function
        elif choice == '4' and logged_in:
            print(check_owned_tickets())
        # calls ticket purchasing function
        elif choice == '5' and logged_in:
            event = int(input("Enter the event ID: "))
            quantity = int(input("Enter the quantity: "))
            result = buy_tickets(event, quantity)
            if "message" in result:
                print(result["message"])
                if "points" in result:
                    print(f"Points: {result['points']}")
        # calls point addition function (ADMIN ONLY)
        elif choice == '6' and logged_in and admin:
            points = int(input("Please enter the amount of points you wish to add: "))
            result = add_points(points)
            if "message" in result:
                print(f"{result["message"]}, points: {result["points"]}")

        # Logout call
        elif choice == '7':
            logged_in = False
        # exit call
        elif choice == '8':
            break


if __name__ == '__main__':
    main()
