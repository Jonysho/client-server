# IRC Server and Client

This project implements a simple IRC (Internet Relay Chat) server and client using Python. The server can handle multiple clients, allowing them to register with a screen name, send messages to all users, send private messages, and see the list of online users.

## Files

- `myserver.py`: The server implementation.
- `myclient.py`: The client implementation.
- `ex2utils.py`: Utility functions and classes for handling socket connections and message processing.

## Requirements

- Python 3.x

## Running the Server

1. Ensure you are in the project directory.
2. Run the server with the following command:
   ```sh
   python3 myserver.py <server_ip> <server_port>