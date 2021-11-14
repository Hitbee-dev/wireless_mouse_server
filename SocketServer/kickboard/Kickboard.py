kickboardDict = {}

class Kickboard():
    def __init__(self, clientData, id):
        self.clientData = clientData
        self.id = id
        self.use = False
        kickboardDict[id] = self
        clientData.closeCallback.append(self.close)

    def close(self):
        print(f"[Pi] kickboard {self.id} disconnected!")
        kickboardDict.pop(self.id)

    