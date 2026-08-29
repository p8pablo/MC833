import threading
from socket import *
import sys  # In order to terminate the program

HOST = ""
PORT = 50007


def client(conn, addr):
    try:
        print(f"Connection established {addr}")
        message = conn.recv(1024)
        if not message:
            return
        print("Received", repr(message))

        filename = message.split()[1]
        f = open(filename[1:], "rb")

        http_status = "HTTP/1.1 200 OK\r\n\r\n".encode()
        content = f.read()

        return_message = http_status + content

        conn.sendall(return_message)
        return

    except Exception:
        # Send response message for file not found
        http_status = "HTTP/1.1 400 Not Found\r\n\r\n".encode()
        print(f"Unexpected error: {Exception}")
        conn.sendall(http_status)

    finally:
        # Close client socket
        conn.close()


s = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Reuse of address
s.bind((HOST, PORT))
s.listen(5)
print("Ready to serve...")


while True:
    # Establish the connection
    conn, addr = s.accept()
    thread = threading.Thread(target=client, args=(conn, addr))
    thread.start()
