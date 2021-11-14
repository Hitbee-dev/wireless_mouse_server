"""
    Title.  main.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        소켓 서버의 진입점 파일입니다.
        config/config.json 파일을 읽어 소켓을 listen 상태로 만듭니다.
"""

import json
import serversocket
from mysql.MySQL import MySQL
import share

config = None

def loadConfig():
    global config
    try:
        with open('./config/config.json') as f:
            config = json.load(f)
    except Exception as e:
        print(e)
        raise Exception('config.json load failed!')

def connectMySQL():
    global config
    share.mysql = MySQL(config["mysql"])
    share.mysql.connect()

def main():
    loadConfig()
    connectMySQL()
    serverSock = serversocket.createSocket()
    serversocket.listenSocket(serverSock, config["socket"]["host"], config["socket"]["port"])

if __name__ == "__main__":
    main()