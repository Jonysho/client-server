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

class MyServer(Server):
    def onStart(self):
        self.connected = 0
        self.clients = {} # {screen: socket}
      
    def onStop(self):
        pass

    def onConnect(self, socket):
        self.connected += 1
        self.printOutput("New client connected")
        self.printOutput(f"{self.connected} active connected")

    def register(self, socket, parameters):
        if len(parameters) != 1:
            return "error invalid parameters"
        screen_name = parameters[0]
        if socket.screen_name:
            socket.send("Error: Already registered".encode())
        elif screen_name in self.clients:
            socket.send("Error: Screen name already taken".encode())
        else:
            self.clients[screen_name] = socket
            socket.screen_name = screen_name
            self.printOutput(f"{screen_name} registered")
            socket.send(f"Welcome, {screen_name}!".encode())
            print(self.clients)

    def onMessage(self, socket, message):
        # <COMMAND> <PARAMETERS>
        pair = message.strip().split(' ')
        command = pair[0].lower()
        if command == "register":
            self.register(socket, pair[1:])
        else:
            print(f"Unknown command: {command}")

        # self.printOutput(f"Message received: {message}")
        return True

    def onDisconnect(self, socket):
        self.connected -= 1
        self.printOutput(f"{self.connected} active connected")
    

ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = MyServer()

# If you want to be an egomaniac, comment out the above command, and uncomment the
# one below...
# server = EgoServer()

# Start server
server.start(ip, port)