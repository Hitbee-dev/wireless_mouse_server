"""
    Title.  client/ClientData.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        클라이언트 소켓 정보 보관을 담당하는 부분입니다.
"""
from packet.Protocol import Encode

clientList = []

class ClientData():
    def __init__(self, socket, addr):
        self.socket = socket
        self.ip = addr[0]
        self.index = addr[1]
        self.buff = b''
        self.closeCallback = []

    def sendPacket(self, data):
        self.socket.send(Encode(data))

    def close(self):
        for func in self.closeCallback:
            func()
        self.socket.close()
