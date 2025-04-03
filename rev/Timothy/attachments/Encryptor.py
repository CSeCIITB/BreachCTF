
def pretty(arr):
    return ''.join(map(str, arr))

def convertBinStrToStr(binStr):

    bytesStr = [binStr[i:i+8] for i in range(0, len(binStr), 8)]
    outStr = ''.join([chr(int(byte, 2)) for byte in bytesStr])
    return outStr

    

class Encryptor:
    def __init__(self, rules):
        self.oldStates = []
        self.currentStates = []
        self.currentStateBuffer = []
        self.rulesToDoStuff = rules
        self.statesCount = 0
        
        pass
    def initialize(self, prevState: str, stringToEncrypt):
        ivBinStr = ''.join(format(ord(i), '08b') for i in prevState)
        binStr = ''.join(format(ord(i), '08b') for i in stringToEncrypt)

        
        self.statesCount = max(len(ivBinStr), len(binStr))
        self.currentStates = [0 for _ in range(self.statesCount)]
        self.oldStates = self.currentStates[:]
        self.currentStateBuffer = self.currentStates[:]
        
        
      
        ivBinStr += '0'*(self.statesCount-len(ivBinStr))
        binStr += '0'*(self.statesCount-len(binStr))
        for i in range(self.statesCount):
            self.oldStates[i] = int(ivBinStr[i])
            self.currentStates[i] = int(binStr[i])
            self.currentStateBuffer[i] = self.currentStates[i]
        
        
    def calcNextState(self):
        self.statesCount = len(self.currentStates)
        radius =  (len(seREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        radiREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED

            if state in self.rulesToDoStuff:
        radiREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTED
        REDACTEDREDACTEDREDACTEDREDACTEDREDACTEDREDACTED
    
    def syncBuffer(self):
        for i in range(self.statesCount):
            self.oldStates[i] = self.currentStates[i]
        for i in range(self.statesCount):
            self.currentStates[i] = self.currentStateBuffer[i]
            
    def iterate(self, iterations):
        for i in range(iterations):
            self.calcNextState()
            self.syncBuffer()
        return self.oldStates, self.currentStates
    
    def getOutput(self, type=0):
        if(type==1):
            return ''.join(map(str, self.currentStateBuffer))
        return  convertBinStrToStr(''.join(map(str, self.currentStates)))
    def getOldOutput(self, type=0):
        if(type==1):
            return ''.join(map(str, self.oldStates))
        return  convertBinStrToStr(''.join(map(str, self.oldStates)))
        
            
            
            
                
                
            

