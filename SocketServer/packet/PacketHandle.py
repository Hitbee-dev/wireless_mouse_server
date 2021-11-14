import share
import cv2
import numpy as np
import segmentation.predict
import time
from packet.PacketCreator import PacketCreator
from kickboard.Kickboard import Kickboard, kickboardDict
from user.UserData import UserData, userDict

def user_login(clientData, data):
    id = data["id"]
    pw = data["pw"]


def user_register(clientData, data):
    mysql = share.mysql
    id = data["id"]
    pw = data["pw"]
    rows = mysql.query(f"SELECT * FROM user_information WHERE id='{id}';")
    print(rows)
    if len(rows) > 0:
        clientData.sendPacket(PacketCreator.dialog('already id !!'))
    else:
        clientData.sendPacket(PacketCreator.dialog('register success !!'))


def kickboard_request(clientData, data):
    code = data["code"]
    if code in kickboardDict:
        if kickboardDict[code].use == True:
            clientData.sendPacket(PacketCreator.kickboardReq(1))
            return
        kickboardDict[code].use = True
        kickboardDict[code].clientData.sendPacket(PacketCreator.kickboardReq(2))
        clientData.sendPacket(PacketCreator.kickboardReq(2))
    else:
        clientData.sendPacket(PacketCreator.kickboardReq(0))

def kickboard_return(clientData, data):
    code = data["code"]
    if code in kickboardDict:
        if (kickboardDict[code].use == True):
            kickboardDict[code].clientData.sendPacket(PacketCreator.kickboardRegion(clientData.index))
            UserData(clientData)
        else:
            clientData.sendPacket(PacketCreator.kickboardRet(1))
            clientData.sendPacket(PacketCreator.dialog(1))
    else:
        clientData.sendPacket(PacketCreator.kickboardRet(0))

def kickboard_region(clientData, data):
    code = data["code"]
    useridx = data["useridx"]
    if code in kickboardDict:
        if (kickboardDict[code].use == True):
            kickboardDict[code].use = False
            kickboardDict[code].clientData.sendPacket(PacketCreator.kickboardRet(2))
            userDict[useridx].clientData.sendPacket(PacketCreator.kickboardRet(2))
            



def pi_connect(clientData, data):
    code = data["code"]
    Kickboard(clientData, code)
    print(f"[Pi] Kickboard connected {code}")
    #kickboardDict[code].clientData.sendPacket(PacketCreator.kickboardRegion(clientData.index))

def pi_capture(clientData, data):
    useridx = data["useridx"]
    code = data["code"]
    strData = data["strData"]
    distance = data["distance"]
    shape = (data["width"], data["height"], 3)
    imgdata = np.array(strData.split(","), dtype="uint8")
    imgdata = np.reshape(imgdata, shape)
    print(imgdata.shape)
    print(distance)
    cv2.imwrite('./segmentation/test/jpgs/test.jpg', imgdata)
    if distance == -1:
        userDict[useridx].clientData.sendPacket(PacketCreator.dialog(2))
    elif (segmentation.predict.main()):
        if code in kickboardDict:
            if (kickboardDict[code].use == True):
                kickboardDict[code].use = False
                kickboardDict[code].clientData.sendPacket(PacketCreator.kickboardRet(2))
                userDict[useridx].clientData.sendPacket(PacketCreator.dialog(1))
                time.sleep(1)
                userDict[useridx].clientData.sendPacket(PacketCreator.kickboardRet(2))