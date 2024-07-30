import socket
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

DARK_GREY = "#121212"
MEDIUM_GREY = "#1F1B24"
OCEAN_BLUE = "#464EB8"
FONT = ("Helvetica", 17)
SMALL_FONT = ("Helvetica", 13)
WHITE = "#FFFFFF"
BUTTON = ("Helvetica", 14)

# Creating socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 3536

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n")
    message_box.config(state=tk.DISABLED)
    message_box.yview(tk.END)

def connect():
    # Connect to the server
    try:
        client.connect((host, port))
        print(f"Successfully connected to {host}:{port}")
        add_message("[SERVER] Successfully connected to the server.")
    except Exception as e:
        messagebox.showerror("Unable to connect to the server", f"Unable to connect to the server: {e}")
        exit(0)
    
    username = username_textbox.get()
    if username:
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty. Exiting...")
        client.close()
        return
    
    # Start the listening thread
    threading.Thread(target=listen_for_messages_from_server, args=(client,), daemon=True).start()
    
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send():
    try:
        message = message_textbox.get()
        if message:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            final_msg = f"[{timestamp}] You - {message}"
            add_message(final_msg)
            client.sendall(message.encode())
            message_textbox.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Message cannot be empty")
    except Exception as e:
        print(f"Error sending message: {e}")
        client.close()

def clear_textbox():
    message_textbox.delete(0, tk.END)

def disconnect():
    client.close()
    root.quit()

root = tk.Tk()
root.geometry("600x600")
root.title("Abhipsa Chat Application")
root.resizable(False, False)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

# Frames are used to divide root window into different sections
top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter Username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=5)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=30)
message_textbox.pack(side=tk.LEFT, padx=4)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON, bg=OCEAN_BLUE, fg=WHITE, command=send)
message_button.pack(side=tk.LEFT, padx=1)

clear_button = tk.Button(bottom_frame, text="Clear", font=BUTTON, bg=OCEAN_BLUE, fg=WHITE, command=clear_textbox)
clear_button.pack(side=tk.LEFT, padx=1)

exit_button = tk.Button(bottom_frame, text="Exit", font=BUTTON, bg=OCEAN_BLUE, fg=WHITE, command=disconnect)
exit_button.pack(side=tk.LEFT, padx=1)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=57, height=28.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                add_message(message)
            else:
                messagebox.showerror("Error", "Received an empty message from the server.")
        except Exception as e:
            print(f"Error receiving message: {e}")
            client.close()
            break

# Main function
def main():
    root.mainloop()

if __name__ == '__main__':
    main()
