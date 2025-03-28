"""

IRC client exemplar.

To run the client:
1. Ensure the server is running.
2. Run the client with the command: python3 myclient.py <server_ip> <server_port>
3. Follow the prompts to register a screen name and send messages.
4. To disconnect, type 'exit'.

Example:
python3 myclient.py localhost 3000
"""

import sys
from ex2utils import Client
import time
import json


class IRCClient(Client):
    
    def onMessage(self, socket, message):
        # Process incoming messages here
        response = json.loads(message)
        self.received_message = response
        if response["type"] == "error":
            print(f"Error: {response['message']}")
        else:
            print(response["message"])
        return True
      
    def register(self):
        while True:
            screen_name = input("Enter screen name: ")
            self.send(f"register {screen_name}".encode())
            if self.received_message["type"] == "success":
                break
        self.send_message()

    def send_message(self):
        while True:
            message = input()
            self.send(message.encode())
            time.sleep(0.5)
            if self.received_message["message"] == "Client exiting":
                break
        self.stop()

# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an IRC client.
client = IRCClient()

# Start client
client.start(ip, port)

# Register screen name
client.register()