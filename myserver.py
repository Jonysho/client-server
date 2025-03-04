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
    clients = set() # set of connected clients

    def onStart(self):
        pass
      
    def onStop(self):
        pass

    def onConnect(self, socket):
        self.clients.add(socket)
        self.printOutput("New client connected")
        self.printOutput(f"{len(self.clients)} active connected")

    def onMessage(self, socket, message):
        # message = message.encode()
        # socket.send(message)
        self.printOutput(f"Message received: {message}")

    def onDisconnect(self, socket):
        self.clients.remove(socket)
        self.printOutput(f"{len(self.clients)} active connected")
    

ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = MyServer()

# If you want to be an egomaniac, comment out the above command, and uncomment the
# one below...
# server = EgoServer()

# Start server
server.start(ip, port)