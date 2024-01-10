# Server for Selling Event Tickets
This project focuses on implementing defensive programming principles to develop a server equipped with robust error checking capabilities. The technology stack for this project includes Python, Flask, and Loguru.

## Technologies Used
Python
Flask
Loguru

##Project Overview
I've successfully developed two separate programs that communicate with each other to facilitate the sale of tickets for a fictitious event. The project leverages the Flask module to establish a server with endpoints where specific JSON data is transmitted. Users can employ the ticket client program to access functions by providing inputs, which are then sent to the corresponding endpoint as JSON requests.

Upon receiving the JSON data, the client processes it based on the targeted endpoint. Subsequently, the server responds with its own JSON data, which the client interprets to retrieve the response and message to display.

## Challenges Faced
I encountered initial challenges in understanding Flask, particularly its capability to process different actions within a function or endpoint, such as handling POST and GET requests using conditional statements. Additionally, configuring a JSON file for a makeshift database and implementing endpoint encryption presented complexities.

## Future Developments
My future plans involve revisiting this project, either with the same technology stack or incorporating additional technologies as my knowledge grows. I aim to enhance security measures by implementing password salting and hashing. Furthermore, I intend to establish an encrypted connection using the existing technology. Exploring the setup of databases such as MySQL, SQLite, or MongoDB for the server is also on my agenda to create a more robust server environment.
