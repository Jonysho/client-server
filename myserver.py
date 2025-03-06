"""
  onStart(self)
      This is called when the server starts - i.e. shortly after the start() method is
      executed. Any server-wide variables should be created here.
      
  onStop(self)
      This is called just before the server stops, allowing you to clean up any server-
      wide variables you may still have set.
      
  onConnect(self, socket)
      This is called when a client starts a new connection with the server, with that
      connection's socket being provided as a parameter. You may store connection-
      specific variables directly in this socket object. You can do this as follows:
          socket.myNewVariableName = myNewVariableValue      
      e.g. to remember the time a specific connection was made you can store it thus:
          socket.connectionTime = time.time()
      Such connection-specific variables are then available in the following two
      events.

  onMessage(self, socket, message)
      This is called when a client sends a new-line delimited message to the server.
      The message paramater DOES NOT include the new-line character.

  onDisconnect(self, socket)
      This is called when a client's connection is terminated. As with onConnect(),
      the connection's socket is provided as a parameter. This is called regardless of
      who closed the connection.
"""
import sys
from ex2utils import Server
import json

class MyServer(Server):
    def onStart(self):
        self.connected = 0
        self.clients = {} # {screen: socket}
      
    def onStop(self):
        pass

    def onConnect(self, socket):
        self.connected += 1
        socket.screen_name = None
        self.printOutput("New client connected")
        self.printOutput(f"{self.connected} active connected")

    def send_error(self, socket, message):
        response = json.dumps({"type": "error", "message": message})
        socket.send(response.encode())

    def send_success(self, socket, message):
        response = json.dumps({"type": "success", "message": message})
        socket.send(response.encode())

    def register(self, socket, params):
        if socket.screen_name:
            self.send_error(socket, "You are already registered")
            return False
        parts = params.split(" ")
        if len(parts) != 1 or not parts[0]:
            self.send_error(socket, "Usage is 'register <screen_name>'")
            return False
        screen_name = parts[0].capitalize()
        if screen_name in self.clients:
            self.send_error(socket, "Screen name already in use")
            return False
        self.clients[screen_name] = socket
        socket.screen_name = screen_name
        self.send_success(socket, f"Welcome, {screen_name}!")
        return True
    
    def send_all(self, socket, params):
        if socket.screen_name is None:
            self.send_error(socket, "You must register first")
            return False
        if not params:
            self.send_error(socket, "Usage is 'send_all <message>'")
            return False
        message = f"Message from {socket.screen_name}: " + params
        for s in self.clients.values():
            if s == socket:
                continue
            self.send_success(s, message)
        return True

    def send_private(self, socket, params):
        if socket.screen_name is None:
            self.send_error(socket, "You must register first")
            return False
        parts = params.split(" ", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            self.send_error(socket, "Usage is 'send_private <screen_name> <message>'")
            return False
        screen_name, message = parts
        screen_name = screen_name.capitalize()
        if screen_name not in self.clients:
            self.send_error(socket, "Screen name not found")
            return False
        if screen_name == socket.screen_name:
            self.send_error(socket, "You can't send a private message to yourself")
            return False
        self.send_success(self.clients[screen_name], f"Private message from {socket.screen_name}: {message}")
        return True

    def onMessage(self, socket, message):
        parts = message.strip().split(' ', 1)
        command = parts[0]
        params = parts[1] if len(parts) > 1 else ""
        if command.lower() == "register":
            self.register(socket, params)
        elif command.lower() == "send_all":
            self.send_all(socket, params)
        elif command.lower() == "send_private":
            self.send_private(socket, params)
        elif command.lower() == "online":
            if not self.clients:
                self.send_success(socket, "No online users")
            else:
                output = f"Online users ({len(self.clients)}): "+", ".join(self.clients)
                self.send_success(socket, output)
        elif command.lower() == "dc":
            self.send_success(socket, "Client exiting")
            return False
        else:
            self.send_error(socket, "unknown command")

        # self.printOutput(f"Message received: {message}")
        return True

    def onDisconnect(self, socket):
        self.connected -= 1
        if socket.screen_name:
            self.clients.pop(socket.screen_name)
            self.printOutput(f"{socket.screen_name} disconnected")
        self.printOutput(f"{self.connected} active connected")
        socket.close()
    

ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()

# Start server
server.start(ip, port)