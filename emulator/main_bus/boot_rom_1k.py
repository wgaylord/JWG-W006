import struct
import mmap

NAME = "Boot Read Only Memory - 1K"

BASE_ADDRESS = 0x0
END_ADDRESS = 0x3FF

rom_mm = None

def init():
    global rom_mm
    rom_file = open("roms/boot.bin","rb")
    rom_mm = mmap.mmap(rom_file.fileno(), 0,prot=mmap.PROT_READ)
    

def readByte(address):
    if address >= BASE_ADDRESS and address <= END_ADDRESS and len(rom_mm) > (address - BASE_ADDRESS):
        return rom_mm[address-BASE_ADDRESS]
    else:
        return 0

def readWord(address):
    if address >= BASE_ADDRESS and address <= END_ADDRESS and len(rom_mm) > (address - BASE_ADDRESS):
        if address+1 >= BASE_ADDRESS and address+1 <= END_ADDRESS and len(rom_mm) > (address+1 - BASE_ADDRESS):
            return struct.unpack("<H",rom_mm[address:address+2])[0]
    else:
        return 0

def writeByte(address,value):
    pass

def writeWord(address,value):
    pass        
    
def tick():
    pass
    
def checkINT():
    return []
