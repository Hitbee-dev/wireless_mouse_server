"""
    Title.  serversocket.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        소켓 발급 및 listen과 소켓 연결 끊김을 감지하는 부분입니다.
        각 소켓은 멀티스레드로 작동합니다.
"""
import socket
from packet import PacketManager as Manager
from _thread import *
from client.ClientData import ClientData, clientList

def createSocket():
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return serverSock

def listenSocket(serverSock, host, port):
    print(host, port)
    serverSock.bind(('', port))
    serverSock.listen()

    # Server Start
    print(f"Server started port '{port}'")
    while True:
        clientSock, addr = serverSock.accept()
        # add Thread
        start_new_thread(socketThread, (clientSock, addr))

def socketThread(clientSock, addr):
    print(f"Connected client {addr[0]}:{addr[1]}")
    clientData = ClientData(clientSock, addr)
    clientList.append(clientData)
    
    while True:
        try:
            if not Manager.recv(clientData):
                break
        except ConnectionResetError as e:
            break
    print(f"Disconnected client {addr[0]}:{addr[1]}")
    clientData.close()
    clientList.remove(clientData)
