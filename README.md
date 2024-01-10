# Event Ticket Selling Server
This is a defensive programming project that requires us to create a server that
has proper error checking and which ever technology we would like.

## Technologies
1. Python
2. Flask
3. Loguru

## What did I do?
I created two seperate programs that are to interact to with each other to sell 
event tickets for a ***made up*** event. The project utilizes the Flask Module
to create a server that has endpoints where the specific json data is sent to.
This allows the user to utilize the ticket client program to all functions that 
take the inputs from the client and sends the data to the endpoint by building the json request and sending it over.

The client then receives the json data and starts processing it depending on which
endpoint the data was sent to. After the data is processed the server responds with their own 
json data that the client processes to get their response and message to display to the client.

## Challenges
Some of the initial challenges I have had were learning how to use Flask itself.
I learned quickly that Flask was a initially harder to understand because within the 
function/endpoint itself you can have it process seperately what happens if you do a 
POST request or a GET request utilizing if statements. Another challenge that I was understanding
how to properly set up a json file for a makeshift database. Setting up endpoint encryption was
kind of hard as well.

## Future Plans
I plan on recreating this again using the same technology or more after I gained a little more knowledge.
I want to be able to do this and implement salting and hashing of passwords as well as creating a encrypted connection
utilizing the technology. One of the other things I would like to learn is how to setup a MySQL or SQLite or 
MongoDB database for the server so that I can feel **MORE** like a server.
