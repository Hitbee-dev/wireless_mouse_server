"""
    Title.  packet/packetManager.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        패킷 상수를 정의하고, 소켓 응답을 받는 부분입니다.
"""
import packet
import share
import numpy as np
import pyautogui as pag
import cv2
import random
import datetime
from packet.PacketCreator import PacketCreator
from packet.Protocol import Decode, HEADER_SIZE
from client.ClientData import ClientData, clientList
from PIL import Image


#{ PACKET_PART
DIALOG          = 3
MOUSE_GESTURE  = 5
MOUSE_LEFT_CLICK = 10
MOUSE_RIGHT_CLICK = 11
MOUSE_DOUBLE_CLICK = 12

CAMERA_IMAGES = 7

#} END PACKET_PART
imgData = []
imgProcess = []
idx = 0

def convertImage(byteImage):
    imgStream = np.uint8(byteImage)
    img = cv2.imdecode(imgStream, cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray_img.shape
    resize = 100
    rx, ry = (w // 2 - resize // 2, h // 2 - resize // 2)
    rect_img = gray_img[rx:rx+resize, ry:ry+resize].copy()
    mosaic_img = mosaic(rect_img, 0.1)
    norm_lv = 1
    norm_img = mosaic_img // norm_lv * norm_lv
    return Image.fromarray(norm_img)


ERROR = 1000
AREA = 2*2
MAXAREA = 10*10

def tracking(src, tgt):
    src_img = src.load()
    tgt_img = tgt.load()
    match = []
    moc_size = 10
    sw, sh = src.width // moc_size, src.height // moc_size
    tw, th = tgt.width // moc_size, tgt.height // moc_size
    tx, ty = -tw, -th

    detectArea = [0, 0]
    for m in range(2, th * 2 - 2):
        ry = ty + m
        detectArea[0] = ry
        if ry < 0: ry = -ry
        else: ry = 0
        for n in range(2, tw * 2 - 2):
            rx = tx + n
            detectArea[1] = rx
            if rx < 0: rx = -rx
            else: rx = 0
            errCount = 0
            for sy in range(max(0, ty + m), min(sh, ty + m + th)):
                for sx in range(max(0, tx + n), min(sw, tx + n + tw)):
                    srcPix = src_img[sx * moc_size, sy * moc_size]
                    tgtPix = tgt_img[(rx + sx) * moc_size, (ry + sy) * moc_size]
                    if srcPix == tgtPix:
                        pass
                    elif errCount < ERROR:
                        errCount += 1
                    else:
                        break
                    #print(f"src : {sx},{sy}", src_img[sx * moc_size, sy * moc_size])
                    #print(f"tgt : {rx + sx},{ry + sy}", tgt_img[(rx + sx) * moc_size, (ry + sy) * moc_size])
                    #print()
            area = (tw - abs(detectArea[1])) * (th - abs(detectArea[0]))
            if area >= AREA:
                match.append([detectArea[1], detectArea[0], area, errCount, (area / MAXAREA) * (1 - errCount / area)])
    res = list(map(lambda l: l[4], match))
    maximum = max(res)
    idxs = list(filter(lambda i: res[i] == maximum, range(len(res))))
    random.shuffle(idxs)
    res = match[idxs[0]]
    print(res)
    mx, my = pag.position()
    ratio = 10
    pag.moveTo(mx-res[0]*ratio, my-res[1]*ratio, _pause=False)

# Broadcast
def broadcast(packet):
    for c in clientList:
        c.sendPacket(packet)

# Packet receiver
def recv(clientData):
    rbuff = clientData.socket.recv(1024)
    if not rbuff:
        return False
    # Check protocol
    clientData.buff += rbuff
    while len(clientData.buff) > 0:
        psize = int(str(clientData.buff[:HEADER_SIZE], encoding='utf-8'))
        if len(clientData.buff) >= psize + HEADER_SIZE:
            data = Decode(clientData.buff[HEADER_SIZE:psize + HEADER_SIZE])
            clientData.buff = clientData.buff[psize + HEADER_SIZE:]
            datacase(clientData, data)
        else:
            break

    return True

def mosaic(src, ratio=0.1):
    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def datacase(clientData, data):
    global imgData, imgProcess, idx
    mysql = share.mysql
    part = data["part"]
    
    if (part == DIALOG):
        clientData.sendPacket(PacketCreator.picapture())

    if (part == MOUSE_GESTURE):
        #print(data)
        # old_moude_x, old_moude_y = pag.position()
        x, y = data["y"], (375 - data["x"])
        w, h = 812, 375
        scw, sch = 2560, 1440

        x, y = scw * x / w, sch * y / h
        print(x, y)
        pag.moveTo(x, y, _pause=False)

    if (part == CAMERA_IMAGES):
        img = data["img"]
        if data["start"] == 1:
            imgData = []
            imgData.append(img)
        elif data["start"] == 2:
            img = convertImage(imgData)
            img.save(f"./img/{datetime.datetime.now().strftime('%H%M%S_%f')}.png")
            idx += 1
            imgProcess.append(img)
            if len(imgProcess) > 2:
                imgProcess.pop(0)
                tracking(imgProcess[0], imgProcess[1])
            
        else:
            imgData.append(img)

    if (part == MOUSE_LEFT_CLICK):
        if (data["click"] == 0):
            pag.click(button='left')

    if (part == MOUSE_RIGHT_CLICK):
        if (data["click"] == 1):
            pag.click(button='right')

    if (part == MOUSE_DOUBLE_CLICK):
        if (data["click"] == 2):
            pag.doubleClick()


