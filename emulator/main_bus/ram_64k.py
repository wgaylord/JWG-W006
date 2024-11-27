import struct

NAME = "Random Access Memory 64K"

BASE_ADDRESS = 0x400
END_ADDRESS = 0x103ff

data = bytearray()

def init():
    for x in range((END_ADDRESS - BASE_ADDRESS)+1):
        data.append(0)
    
def readByte(address):
    if address >= BASE_ADDRESS and address >= BASE_ADDRESS and len(data) > (address - BASE_ADDRESS):
        return data[address-BASE_ADDRESS]
    else:
        return 0

def readWord(address):
    if address >= BASE_ADDRESS and address <= END_ADDRESS and len(data) > (address - BASE_ADDRESS):
        if address+1 >= BASE_ADDRESS and address+1 <= END_ADDRESS and len(data) > (address+1 - BASE_ADDRESS):
            return struct.unpack("<H",data[(address - BASE_ADDRESS):(address - BASE_ADDRESS)+2])[0]
    else:
        return 0

def writeByte(address,value):
    if address >= BASE_ADDRESS and address <= END_ADDRESS and len(data) > (address - BASE_ADDRESS):
        data[address-BASE_ADDRESS] = value & 0xff

def writeWord(address,value):
    if address >= BASE_ADDRESS and address <= END_ADDRESS and len(data) > (address - BASE_ADDRESS):
        if address+1 >= BASE_ADDRESS and address+1 <= END_ADDRESS and len(data) > (address+1 - BASE_ADDRESS):
            data[(address - BASE_ADDRESS):(address - BASE_ADDRESS)+2] = struct.pack("<H",value)
  
         
def tick():
    pass
    
def checkINT():
    return []
