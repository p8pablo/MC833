from socket import *
import sys # In order to terminate the program
HOST = ''
PORT = 50007

s = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket

s.bind((HOST,PORT))
s.listen(1)
print('Ready to serve...')
conn, addr = s.accept()

with conn:
    print(f'Connection established {conn}')

    while True:
        #Establish the connection

        try:
            conn.sendall(b'Hello World')
            message = conn.recv(1024)
            if not message: break
            print('Received', repr(message))
            # filename = message.split()[1]
            # f = open(filename[1:])
            # output_data = f
            #Send one HTTP header line into socket


            #Send the content of the requested file to the client

            # for i in range(0, len(outputdata)):
            #    conn.send(outputdata[i].encode())
            # conn.send("\r\n".encode())

            conn.close()
        except IOError:
            #Send response message for file not found
            print(f'Unexpected error: {IOError}')

            #Close client socket


    s.close()
    sys.exit()#Terminate the program after sending the corresponding data