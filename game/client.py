import socket
import pickle
import random

def generate_server_choice():
    choices = ["Rock", "Paper", "Scissors"]
    return random.choice(choices)

def calculate_result(client_choice, server_choice):
    if client_choice == server_choice:
        return "Draw"
    elif (client_choice == "Rock" and server_choice == "Scissors") or \
         (client_choice == "Paper" and server_choice == "Rock") or \
         (client_choice == "Scissors" and server_choice == "Paper"):
        return "You Win!"
    else:
        return "You Lose!"

def main():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the server socket to a specific address and port
    server_socket.bind(('localhost', 12345))
    # Listen for incoming connections
    server_socket.listen(1)
    print("Server started. Waiting for a client to connect...")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Client connected:", client_address)

        try:
            while True:
                # Receive the client's choice
                client_choice = client_socket.recv(1024).decode()
                print("Client's choice:", client_choice)

                # Generate the server's choice
                server_choice = generate_server_choice()
                print("Server's choice:", server_choice)

                # Calculate the result of the game
                result = calculate_result(client_choice, server_choice)
                print("Result:", result)

                # Send the server's choice and the result back to the client
                client_socket.send(pickle.dumps(server_choice))
                client_socket.send(pickle.dumps(result))
        except Exception as e:
            print("Error:", e)
        finally:
            # Close the client socket
            client_socket.close()

if __name__ == '__main__':
    main()
