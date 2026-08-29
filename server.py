from socket import *
import sys  # In order to terminate the program

HOST = ""
PORT = 50007

s = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket

s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Reuse of address

s.bind((HOST, PORT))
s.listen(1)
print("Ready to serve...")


while True:
    # Establish the connection
    conn, addr = s.accept()

    with conn:
        print(f"Connection established {addr}")
        try:
            message = conn.recv(1024)
            if not message:
                continue
            print("Received", repr(message))

            http = "HTTP/1.1 200 OK\r\n\r\n"
            content = "<h1>Hello World!</h1>"

            return_message = http + content

            conn.sendall(return_message.encode())
        except IOError:
            # Send response message for file not found
            print(f"Unexpected error: {IOError}")

            # Close client socket
