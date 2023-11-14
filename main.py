import requests

# Server URL
SERVER_URL = 'http://127.0.0.1:5000'  # Change to your server's URL

username = ""

def register_user(username, password):
    data = {"username": username, "password": password}
    response = requests.post(f'{SERVER_URL}/register', json=data)
    return response.json()


def login_user(username, password):
    data = {"username": username, "password": password}
    response = requests.post(f'{SERVER_URL}/login', json=data)
    return response.json()


def check_available_tickets():
    data = requests.get(f"{SERVER_URL}/check_available_tickets")
    return data.json()


def check_owned_tickets():
    data={"username": username}
    response =  requests.post(f"{SERVER_URL}/check_owned_tickets", json=data)
    return response.json()



def buy_tickets( event, quantity):
    data = {"username": username, "id": event, "quantity": quantity}
    response = requests.post(f'{SERVER_URL}/buy_tickets', json=data)
    return response.json()


def add_points(points):
    data = {"username": username, "points": points}
    response = requests.post(f"{SERVER_URL}/add_points", json=data)
    return response.json()


def main():
    global username
    logged_in = False

    while True:
        if not logged_in:
            print("1. Register")
            print("2. Login")
        else:
            print("3. Check Available Tickets")
            print("4. Check Owned Tickets")
            print("5. Buy Tickets")
            print("6. Add Points")
            print("7. Logout")

        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            result = register_user(username, password)
            print(result["message"])

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            result = login_user(username, password)
            if "message" in result:
                print(result["message"])
                if "points" in result:
                    print(f"Points: {result['points']}")
                    logged_in = True
            else:
                logged_in = False

        elif choice == '3' and logged_in:
            print(check_available_tickets())
            # Implement code to display available tickets

        elif choice == '4' and logged_in:
            print(check_owned_tickets())
            # Implement code to display owned tickets for the user

        elif choice == '5' and logged_in:
            event = int(input("Enter the event ID: "))
            quantity = int(input("Enter the quantity: "))
            result = buy_tickets(event, quantity)
            if "message" in result:
                print(result["message"])
                if "points" in result:
                    print(f"Points: {result['points']}")

        elif choice == '6' and logged_in:
            points = int(input("Please enter the amount of points you wish to add: "))
            result = add_points(points)
            if "message" in result:
                print(f"{result["message"]}, points: {result["points"]}")


        elif choice == '7':
            logged_in = False

        elif choice == '8':
            break


if __name__ == '__main__':
    main()