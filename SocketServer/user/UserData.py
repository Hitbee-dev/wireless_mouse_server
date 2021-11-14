userDict = {}

class UserData():
    def __init__(self, clientData):
        self.clientData = clientData
        self.useCode = None
        userDict[clientData.index] = self
        clientData.closeCallback.append(self.remove)

    def remove(self):
        if self.clientData.index in userDict:
            userDict.pop(self.clientData.index)