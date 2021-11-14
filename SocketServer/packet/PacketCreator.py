"""
    Title.  packet/packetCreator.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        패킷 Encoding 전 Dictionary 형태로 변환하는 부분입니다.
"""
from packet import PacketManager as Manager

class PacketCreator():
    def dialog(msg):
        data = {}
        data["part"] = Manager.DIALOG
        data["msg"] = msg
        return data

    def picapture():
        data = {}
        data["part"] = Manager.PI_CAPTURE
        return data