import struct
import os.path
import pickle

NAME = "C_HDD"

BASE_ADDRESS = 0xC0000400
END_ADDRESS = 0xC000060F

REG_END = BASE_ADDRESS + 8
DATA_START = REG_END + 8


drive = None



data = b''

regs = bytearray()

def init():      

    if not os.path.isfile("roms/chdd.bin"):
        t = open("roms/chdd.bin","wb+")
        pickle.dump({},t)
        t.close()
        
    HDD_FILE = open("roms/chdd.bin","rb")

    drive = pickle.load(HDD_FILE)  
    HDD_FILE.close()
    
    for x in range(9):
        regs.append(0)

def updateFile():
    HDD_FILE = open("roms/chdd.bin","wb+")
    pickle.dump(drive,HDD_FILE)
    HDD_FILE.close()
    
    
def readByte(address):
    global data
    if address >= BASE_ADDRESS and address <= REG_END and len(data) > (address - BASE_ADDRESS):
        if address-BASE_ADDRESS == 6:
            upper = struct.unpack(">H",regs[:2])[0]
            lower = struct.unpack(">I",regs[2:6])[0]
            LBA = (upper << 16) + lower
            if not LBA in drive.keys():
                data = b''
                for x in range(512):
                    data += b"\00"
            else:
                data = drive[LBA]
        return regs[address-BASE_ADDRESS]
    elif address >= DATA_START and address <= END_ADDRESS and len(data) > (address - DATA_START):
        return data[address-DATA_START]
    else:
        return 0

def readWord(address):
    global data
    if address >= BASE_ADDRESS and address <= REG_END and len(data) > (address - BASE_ADDRESS):
        if address+1 >= BASE_ADDRESS and address+1 <= REG_END and len(data) > (address+1 - BASE_ADDRESS):
            if address-BASE_ADDRESS == 6 or( address+1)-BASE_ADDRESS == 6:
                upper = struct.unpack(">H",regs[:2])[0]
                lower = struct.unpack(">I",regs[2:6])[0]
                LBA = (upper << 16) + lower
                if not LBA in drive.keys():
                    data = b''
                    for x in range(512):
                        data += b"\00"
                else:
                    data = drive[LBA]
            return struct.unpack(">H",regs[(address - BASE_ADDRESS):(address - BASE_ADDRESS)+2])[0]
    elif address >= DATA_START and address <= END_ADDRESS and len(data) > (address - DATA_START):
        if address+1 >= DATA_START and address+1 <= END_ADDRESS and len(data) > (address+1 - DATA_START):
            return struct.unpack(">H",data[(address - DATA_START):(address - DATA_START)+2])[0]
    else:
        return 0

def writeByte(address,value):
    if address >= BASE_ADDRESS and address <= REG_END and len(data) > (address - BASE_ADDRESS):
        if address-BASE_ADDRESS == 6:
            upper = struct.unpack(">H",regs[:2])[0]
            lower = struct.unpack(">I",regs[2:6])[0]
            LBA = (upper << 16) + lower
            drive[LBA] = data
            updateFile()
        regs[address-BASE_ADDRESS] = value & 0xff
    elif address >= DATA_START and address <= END_ADDRESS and len(data) > (address - DATA_START):
        data[address-DATA_START] = value & 0xff
    
def writeWord(address,value):
    if address >= BASE_ADDRESS and address <= REG_END and len(data) > (address - BASE_ADDRESS):
        if address+1 >= BASE_ADDRESS and address+1 <= REG_END and len(data) > (address+1 - REG_END):
            if address-BASE_ADDRESS == 6 or( address+1)-BASE_ADDRESS == 6:
                upper = struct.unpack(">H",regs[:2])[0]
                lower = struct.unpack(">I",regs[2:6])[0]
                LBA = (upper << 16) + lower
                drive[LBA] = data
                updateFile()
            reg[(address - BASE_ADDRESS):(address - BASE_ADDRESS)+2] = struct.pack(">H",value)
    elif address >= BASE_ADDRESS and address <= END_ADDRESS and len(data) > (address - BASE_ADDRESS):
        if address+1 >= DATA_START and address+1 <= END_ADDRESS and len(data) > (address+1 - DATA_START):
            data[(address - DATA_START):(address - DATA_START)+2] = struct.pack(">H",value)
  
         
def tick():
    pass
    
def checkINT():
    return []
