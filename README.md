# IRC Server and Client

This project implements a simple IRC (Internet Relay Chat) server and client using Python. The server can handle multiple clients, allowing them to register with a screen name, send messages to all users, send private messages, and see the list of online users.

## Files

- `myserver.py`: The server implementation.
- `myclient.py`: The client implementation.
- `ex2utils.py`: Utility functions and classes for handling socket connections and message processing.

## Requirements

- Python 3.x

## Running the Server
Start the server using:
```bash
python3 myserver.py localhost 8090
```

## Running the Client
Start the client using:
```bash
python3 myclient.py localhost 8090
```

## Testing with Telnet (Optional)
You can test the server manually using telnet:
```bash
telnet localhost 8090
```
Then enter commands according to the protocol.

## Features
- Users must register with a unique username.
- Send messages to all users.
- Send private messages to specific users.
- List online users.
- Graceful client disconnection.

## Protocol Commands
| Command          | Description                                   | Example Usage              |
|-----------------|-----------------------------------------------|----------------------------|
| `register`      | Registers a new user                         | `register JohnDoe`         |
| `send_all`      | Sends a message to all users                 | `send_all Hello everyone!` |
| `send_one`      | Sends a private message to a user            | `send_private Alice Hi Alice!` |
| `online_users`  | Lists all connected users                    | `online`             |
| `close_connection` | Disconnects the client from the server    | `dc`         |