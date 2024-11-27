import struct
import os.path
import pickle

NAME = "C_HDD"

BASE_ADDRESS = 0xC0000400
REG_END = BASE_ADDRESS + 6
DATA_START = 0xC0000410
END_ADDRESS = 0xC0000810 + 1024



drive = None

class Registers:
    def __init__(self):
        pass
    
    LBA0 = 0
    LBA1 = 0
    LBA2 = 0
    LBA3 = 0
    
    ready = True
    invalid_lba = False
    
    command = 0
    
    def writeByte(self,reg,data):
        if reg == 0:
            self.LBA0 = data
        elif reg == 1:
            self.LBA1 = data
        elif reg == 2:
            self.LBA2 = data
        elif reg == 3:
            self.LBA3 = data
        elif reg == 5:
            self.command = data
        
        self.invalid_lba = self.readLBA() <= drive["max_lba"]

    def writeWord(self,reg,data):
        if reg == 0:
            self.LBA0 = data >> 8
            self.LBA1 = data & 0xFF
        elif reg == 1:
            self.LBA1 = data >> 8
            self.LBA2 = data & 0xFF
        elif reg == 2:
            self.LBA2 = data >> 8
            self.LBA3 = data & 0xFF
        elif reg == 3:
            self.LBA3 = data >> 8
            self.command = data & 0xFF
        elif reg == 5:
            self.command = data >> 8
            
        self.invalid_lba = self.readLBA() <= drive["max_lba"]
            
            
    def readByte(self,reg):
        if reg == 0:
            return self.LBA0
        elif reg == 1:
            return self.LBA1
        elif reg == 2:
            return self.LBA2
        elif reg == 3:
            return self.LBA3
        elif reg == 4:
            return self.ready * 0x1 + self.invalid_lba * 0x2
        elif reg == 5:
            return self.command
            
    def readWord(self,reg):
        if reg == 0:
            return (self.LBA0 << 8) + self.LBA1
        elif reg == 1:
            return (self.LBA1 << 8) + self.LBA2
        elif reg == 2:
            return (self.LBA2 << 8) + self.LBA3
        elif reg == 3:
            return (self.LBA3 << 8) + (self.ready * 0x1 + self.invalid_lba * 0x2) 
        elif reg == 4:
            return ((self.ready * 0x1 + self.invalid_lba * 0x2) << 8  ) + self.command
        elif reg == 5:
            return self.command << 8
        

    def readLBA(self):
        return (self.LBA0 << 24) + (self.LBA1 << 16) + (self.LBA2 << 8) + self.LBA3


    def writeLBA(self,value):
        self.LBA0  = value >> 24
        self.LBA1 = (value & 0xFFFFFF) >> 16
        self.LBA2 = (value & 0xFFFF) >> 8
        self.LBA3 = value & 0xFF

data = b''

command = 0

registers  = Registers()

def init():      
    if not os.path.isfile("roms/chdd.bin"):
        t = open("roms/chdd.bin","wb+")
        pickle.dump({"max_lba":0x32000},t) #Deafult disk is 100MB in size or 0x32000 512
        t.close()
        
    HDD_FILE = open("roms/chdd.bin","rb")

    drive = pickle.load(HDD_FILE)  
    HDD_FILE.close()


def updateFile():
    HDD_FILE = open("roms/chdd.bin","wb+")
    pickle.dump(drive,HDD_FILE)
    HDD_FILE.close()
    
    
def readByte(address):
    global data
    return_data = 0
    if address >= BASE_ADDRESS and address <= REG_END and len(data) > (address - BASE_ADDRESS):
        if address-BASE_ADDRESS >= 0 and address-BASE_ADDRESS <= 5:
            return_data =  registers.readByte(address-BASE_ADDRESS)
        if address-BASE_ADDRESS == 6:
            LBA = lba.readLBA()
            if LBA <= drive["max_lba"]:
                if not LBA in drive.keys():
                    data = b''
                    for x in range(512):
                        data += b"\00"
                else:
                    data = drive[LBA]
        return return_data
    elif address >= DATA_START and address <= END_ADDRESS and len(data) > (address - DATA_START):
        return data[address-DATA_START]
    else:
        return 0

def readWord(address):
    global data
    
    return_data = 0
    if address >= BASE_ADDRESS and address <= REG_END and len(data) > (address - BASE_ADDRESS):
        if address+1 >= BASE_ADDRESS and address+1 <= REG_END and len(data) > (address+1 - BASE_ADDRESS):
            if address-BASE_ADDRESS >= 0 and address-BASE_ADDRESS <=5: 
                return_data =  registers.readWord(address-BASE_ADDRESS)
            if address-BASE_ADDRESS == 6 or( address+1)-BASE_ADDRESS == 6:
                LBA = lba.readLBA()
                if LBA <= drive["max_lba"]:
                    if not LBA in drive.keys():
                        data = b''
                        for x in range(512):
                            data += b"\00"
                    else:
                        data = drive[LBA]
        return return_data
    elif address >= DATA_START and address <= END_ADDRESS and len(data) > (address - DATA_START):
        if address+1 >= DATA_START and address+1 <= END_ADDRESS and len(data) > (address+1 - DATA_START):
            return struct.unpack(">H",data[(address - DATA_START):(address - DATA_START)+2])[0]
    else:
        return 0

def writeByte(address,value):
    if address >= BASE_ADDRESS and address <= REG_END and len(data) > (address - BASE_ADDRESS):
        if address-BASE_ADDRESS >= 0 and address-BASE_ADDRESS <=5: 
            registers.writeByte(address-BASE_ADDRESS,value)
        if address-BASE_ADDRESS == 6:
            LBA = lba.readLBA()
            if LBA <= drive["max_lba"]:
                drive[LBA] = data
                updateFile()
    elif address >= DATA_START and address <= END_ADDRESS and len(data) > (address - DATA_START):
        data[address-DATA_START] = value & 0xff
    
def writeWord(address,value):
    if address >= BASE_ADDRESS and address <= REG_END and len(data) > (address - BASE_ADDRESS):
        if address+1 >= BASE_ADDRESS and address+1 <= REG_END and len(data) > (address+1 - REG_END):
            if address-BASE_ADDRESS >= 0 and address-BASE_ADDRESS <=5: 
                registers.writeWord(address-BASE_ADDRESS,value)
            if address-BASE_ADDRESS == 6 or( address+1)-BASE_ADDRESS == 6:
                LBA = lba.readLBA()
                if LBA <= drive["max_lba"]:
                    drive[LBA] = data
                    updateFile()
    elif address >= BASE_ADDRESS and address <= END_ADDRESS and len(data) > (address - BASE_ADDRESS):
        if address+1 >= DATA_START and address+1 <= END_ADDRESS and len(data) > (address+1 - DATA_START):
            data[(address - DATA_START):(address - DATA_START)+2] = struct.pack(">H",value)
  
         
def tick():
    pass
    
def checkINT():
    return []
