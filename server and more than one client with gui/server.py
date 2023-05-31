import socket
import threading
import tkinter as tk

class Server:
    def __init__(self, master, port):
        self.master = master
        self.port = port
        self.socket = None
        self.clients = {}

        # Label to display the server status
        self.status_label = tk.Label(master, text="Server is running on port {}".format(port))
        self.status_label.pack()

        # Button to start the server
        self.start_button = tk.Button(master, text="Start", command=self.start_server)
        self.start_button.pack()

        # Button to stop the server
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack()

    def start_server(self):
        # Create a socket and bind it to the specified port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", self.port))
        self.socket.listen(5)

        # Update the status label and button states
        self.status_label.config(text="Server is running on port {}".format(self.port))
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start accepting client connections in a separate thread
        threading.Thread(target=self.accept_clients).start()

    def accept_clients(self):
        while True:
            # Accept a client connection
            client_socket, address = self.socket.accept()

            # Generate a username for the client and send it to the client
            username = "User{}".format(len(self.clients) + 1)
            client_socket.sendall(username.encode())

            # Create a client dictionary with username and socket
            client = {"username": username, "socket": client_socket}
            self.clients[username] = client

            # Broadcast a message to all clients about the new client joining
            self.broadcast_message("{} has joined the chat.".format(username))

            # Start a separate thread to handle the client's messages
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        username = client["username"]
        socket = client["socket"]

        while True:
            try:
                # Receive a message from the client
                message = socket.recv(1024).decode()
                if not message:
                    break

                # Broadcast the message to all clients
                self.broadcast_message("{}: {}".format(username, message))
            except ConnectionResetError:
                break

        # Remove the client from the list and broadcast a message about client leaving
        self.remove_client(username)

    def remove_client(self, username):
        client = self.clients.pop(username)
        client["socket"].close()

        # Broadcast a message to all clients about the client leaving
        self.broadcast_message("{} has left the chat.".format(username))

    def broadcast_message(self, message):
        # Send the message to all connected clients
        for client in self.clients.values():
            client["socket"].sendall(message.encode())

    def stop_server(self):
        # Close all client sockets and the server socket
        for client in self.clients.values():
            client["socket"].close()

        self.socket.close()
        self.socket = None

        # Update the status label and button states
        self.status_label.config(text="Server stopped.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chat Room Server")

    # Create an instance of the Server class with the root window and port number
    server = Server(root, 8000)

    # Start the Tkinter event loop
    root.mainloop()
