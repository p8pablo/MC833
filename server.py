import threading
from socket import *
import sys  # In order to terminate the program

HOST = ""
PORT = 50007
TIMEOUT_SECONDS = 30


def client(conn, addr):
    try:
        print(f"Connection established {addr}")
        message = conn.recv(1024)
        message = message.decode()
        if not message:
            return
        print("Received", repr(message))

        filename = message.split()[1]
        if filename == "/":
            filename = "/index.html"

        f = open(filename[1:], "rb")

        http_status = "HTTP/1.1 200 OK\r\n\r\n"
        content = f.read()

        return_message = http_status.encode() + content

        conn.sendall(return_message)
        return

    except Exception:
        # Send response message for file not found
        http_status = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        print(f"Unexpected error: {Exception}")
        conn.send(http_status)

    finally:
        # Close client socket
        conn.close()


s = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Reuse of address
s.bind((HOST, PORT))
s.listen(5)
s.settimeout(TIMEOUT_SECONDS)
print("Ready to serve...")


try:
    while True:
        try:
            # Establish the connection
            conn, addr = s.accept()
            thread = threading.Thread(target=client, args=(conn, addr))
            thread.start()
        except timeout:
            print(f"No client connected in {TIMEOUT_SECONDS}. Closing server")
            break
except KeyboardInterrupt:
    print("Closing server due to manual interruption")

finally:
    s.close()
    print("Server closed.")
    sys.exit(0)
