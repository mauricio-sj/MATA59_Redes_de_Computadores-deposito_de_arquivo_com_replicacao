import socket
import threading
import time
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

def start():
    server.listen()
    client, addr = server.accept()
    print("aguardando cliente...")
    file_name = client.recv(1024).decode()
    print(file_name)
    file_size = client.recv(1024).decode()
    print(file_size)
    
    if(file_name.startswith("rec")): 
        pass
    else:
        file = open("copia_" + file_name,"wb")
        file_bytes = b""
        done = False
        while not done:
            data = client.recv(1024)
            if file_bytes[-5:] == b"<END>":
                done = True
            else:
                file_bytes += data
        file.write(file_bytes)
        file.close()
        client.close()
        server.close()
        pass


start()


