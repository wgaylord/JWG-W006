import sys
import threading
import os
import tty
from queue import Queue

NAME = "Output only serial bus"

BASE_ADDRESS = 0xC0000000
END_ADDRESS = 0xC0000005

INTERRUPT_NUMS_STARTING = 16


input_thread = None
input_queue = None

interrupt_settings = 0

did_write = False

def init():
    global input_thread
    global input_queue


def readByte(address):
    if address >= BASE_ADDRESS and address <= END_ADDRESS:
        index = address - BASE_ADDRESS
        if index == 0:
            if not input_queue.empty():
                return  ord(input_queue.get())
            else:
                return 0
        if index == 1:
            return input_queue._qsize()
        if index == 2:
            return 0
        if index == 3:
            return interrupt_settings
    else:
        return 0

def readWord(address):
    if address >= BASE_ADDRESS and address <= END_ADDRESS and len(rom_mm) > (address - BASE_ADDRESS):
        if address+1 >= BASE_ADDRESS and address+1 <= END_ADDRESS and len(rom_mm) > (address+1 - BASE_ADDRESS):
            return (readByte(address) << 16) | readByte(address+1)
    else:
        return 0

def writeByte(address,value):
    if address >= BASE_ADDRESS and address <= END_ADDRESS:
        index = address - BASE_ADDRESS
        if index == 0:
           did_write = True
           sys.stdout.write(chr(value & 0xFF))
           sys.stdout.flush()
        if index == 1:
            pass
        if index == 2:
            pass
        if index == 3:
            interrupt_settings = value
    else:
        return 0

def writeWord(address,value):
    pass
         
def tick():
    pass
    
def checkINT():
    ints = []
    if interrupt_settings & 1 == 1:
        if not self.input_queue.empty():
            ints.append(INTERRUPT_NUMS_STARTING)
    if interrupt_settings & 2 == 2:
        if self.input_queue.full():
            ints.append(INTERRUPT_NUMS_STARTING+1)
    if interrupt_settings & 4 == 4:
        if did_write:
            did_write = False
            ints.append(INTERRUPT_NUMS_STARTING+2)
        
    return ints
