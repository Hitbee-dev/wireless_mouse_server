"""
    Title.  packet/protocol.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        패킷 송/수신에 관한 프로토콜 변환을 담당합니다.

        * Packet
            3byte    1~999byte
            [Header]+[Body]

        * Header
            3byte : body byte length

        * Body
            "'part':type|Key:Value|...|"
        
        * Value (Example)
            integer : \\i1234 (1234)
            float   : \\d12.324 (12.324)
            ":"     : \\cm (:)
            "|"     : \\v (|)
"""
HEADER_SIZE = 8

def Encode(data):
    packet = ""
    for k, v in data.items():
        packet += f"{k}:"
        if str(type(v)) == "<class 'int'>":
            packet += f"\\i"
        elif str(type(v)) == "<class 'float'>":
            packet += f"\\d"
        elif str(type(v)) == "<class 'string'>":
            v = v.replace(":", "\\cm")
            v = v.replace("|", "\\v")
        packet += f"{v}|"
    plen = len(packet.encode('utf-8'))
    packet = (HEADER_SIZE - len(str(plen))) * "0" + f"{plen}{packet}"
    return packet.encode('utf-8')


def Decode(packet):
    data = {}
    packet = packet.decode()
    pdata = packet.split("|")
    for p in pdata:
        part = p.split(":")
        if len(part[0]) < 1:
            continue
        if part[1].find("b\'") != -1:
            part[1] = part[1].encode()
            part[1] = part[1].replace(b'\\cm', b':')
            part[1] = part[1].replace(b'\\v', b'|')
            print(part[1])
            data[part[0]] = part[1]
        elif part[1].find("\\i") != -1:
            data[part[0]] = int(part[1][2:])
        elif part[1].find("\\d") != -1:
            data[part[0]] = float(part[1][2:])
        else:
            part[1] = part[1].replace('\\cm', ':')
            part[1] = part[1].replace('\\v', '|')
            data[part[0]] = part[1]
    return data
