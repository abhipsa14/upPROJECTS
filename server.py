import socket
import threading
from datetime import datetime

host = "127.0.0.1"
port = 3536 # Changed the port number
listener_limit = 5
active_clients = []  # list of all currently connected users

# Function to send any new message to all the clients that are currently connected to this server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to listen for upcoming messages.
def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                final_msg = f"[{timestamp}] {username} - {message}"
                send_messages_to_all(final_msg)
            else:
                print(f"Empty message from the client: {username}")
        except Exception as e:
            print(f"Error: {e}")
            active_clients.remove((username, client))
            client.close()
            break

# Function to send message to a single client
def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to client: {e}")
        client.close()

# Function to handle client
def client_handler(client):
    # Server will listen for client message that will contain the username
    while True:
        try:
            username = client.recv(2048).decode('utf-8')  # Encoding used is utf-8
            if username:
                active_clients.append((username, client))
                break
            else:
                print("Client username is empty")
        except Exception as e:
            print(f"Error receiving username: {e}")
            client.close()
            return
    
    threading.Thread(target=listen_for_messages, args=(client, username), daemon=True).start()

# Main function
def main():
    # Creating server side communication
    # AF_INET: we are using ipv4 address.
    # SOCK_STREAM: TCP Protocol is used
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Two types of networking addresses: ipv4 and ipv6

    # Set the socket options to reuse the address
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Provides the server with an address in the form of host IP and port
        server.bind((host, port))
        print(f"Running on {host}:{port}")
    except Exception as e:
        print(f"Unable to bind to host {host} and port {port}: {e}")
        return
    
    # Setting server limit
    server.listen(listener_limit)
    
    # This loop will keep listening to the client.
    while True:
        client, address = server.accept()
        print(f"Successfully connected to client - {address[0]}:{address[1]}")
        threading.Thread(target=client_handler, args=(client,), daemon=True).start()

if __name__ == '__main__':
    main()
