
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
        # self.cellCount = cellCount
        self.rulesToFlip = rules
        self.cellCount = 0
        
        pass
    def initialize(self, prevState: str, stringToEncrypt):
        ivBinStr = ''.join(format(ord(i), '08b') for i in prevState)
        binStr = ''.join(format(ord(i), '08b') for i in stringToEncrypt)

        
        self.cellCount = max(len(ivBinStr), len(binStr))
        self.currentStates = [0 for _ in range(self.cellCount)]
        self.oldStates = self.currentStates[:]
        self.currentStateBuffer = self.currentStates[:]
        
        
      
        ivBinStr += '0'*(self.cellCount-len(ivBinStr))
        binStr += '0'*(self.cellCount-len(binStr))
        # print(len(binStr))
        for i in range(self.cellCount):
            self.oldStates[i] = int(ivBinStr[i])
            self.currentStates[i] = int(binStr[i])
            self.currentStateBuffer[i] = self.currentStates[i]
        
        
    def calcNextState(self):
        self.cellCount = len(self.currentStates)
        radius =  (len(self.rulesToFlip[0])-1)//2
        for i in range(self.cellCount):
            cellStates = ""
            for j in range(-radius, radius+1):
                idx = (i+j)%self.cellCount
                cellStates += str(self.currentStates[idx])

                    

            if cellStates in self.rulesToFlip:
                self.currentStateBuffer[i] = 1-int(self.oldStates[i])
            else:
                self.currentStateBuffer[i] = self.oldStates[i]
    
    def syncBuffer(self):
        for i in range(self.cellCount):
            self.oldStates[i] = self.currentStates[i]
        for i in range(self.cellCount):
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
        
            
            
            
                
                
            

