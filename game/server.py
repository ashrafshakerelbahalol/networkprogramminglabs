import socket
import pickle
import tkinter as tk
from tkinter import messagebox

def send_choice(choice):
    try:
        # Send the client's choice to the server
        client_socket.send(choice.encode())
        # Receive the server's choice
        server_choice = pickle.loads(client_socket.recv(1024))
        # Receive the result of the game
        result = pickle.loads(client_socket.recv(1024))
        # Display the server's choice and the result in a message box
        messagebox.showinfo("Result", f"Server's choice: {server_choice}\nResult: {result}")
    except Exception as e:
        # Display an error message in case of an error
        messagebox.showerror("Error", str(e))

def main():
    global client_socket
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the client socket to the server
    client_socket.connect(('localhost', 12345))

    # Create a GUI window
    root = tk.Tk()
    root.title("Rock, Paper, Scissors Game")

    # Create buttons for the game choices
    rock_button = tk.Button(root, text="Rock", command=lambda: send_choice("Rock"))
    rock_button.pack()

    paper_button = tk.Button(root, text="Paper", command=lambda: send_choice("Paper"))
    paper_button.pack()

    scissors_button = tk.Button(root, text="Scissors", command=lambda: send_choice("Scissors"))
    scissors_button.pack()

    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    main()
