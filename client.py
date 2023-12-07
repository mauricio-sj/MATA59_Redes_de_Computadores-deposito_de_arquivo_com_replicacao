import os
import socket
import threading
import time


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))
         

def start():
    print("O que deseja acessar? \n 1 - Depósito \n 2 - recuperação")
    acesso = int(input())
    if acesso == 1:
        print("Qual o arquivo que deseja depositar?")
        arq = input()
        file = open(arq, "rb")
        file_size = os.path.getsize(arq)
        client.send(arq.encode())
        client.send(str(file_size).encode())
        time.sleep(0.1)
        data = file.read()
        client.sendall(data)
        client.send(b"<END>")
    elif acesso == 2:
        print("Qual o arquivo que deseja recuperar?")
        arq = input()
        file = open(arq, "rb")
        file_size = os.path.getsize(arq)
        client.send(("rec" + arq).encode())
        client.send((str(file_size)).encode())
    else:
        print("código inválido, reiniciando...")
        start()
    
        
        


start()

