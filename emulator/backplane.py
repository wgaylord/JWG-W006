import importlib
import pkgutil

import main_bus


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

discovered_cards = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(main_bus)
}

def init():

    print("    Initalizing Devices on Main Bus.")
    print("    ================================")
    
    for x in discovered_cards.keys():
        if not x.startswith("main_bus._"):
            print("      Initalizing " + discovered_cards[x].NAME+".")
            discovered_cards[x].init()
        else:
            print("      Skipping " + discovered_cards[x].NAME + " because it is disabled.")



def readByte(address):
    
    data = 0
    for x in discovered_cards.keys():
        if not x.startswith("main_bus._"):
            data |= discovered_cards[x].readByte(address)
    #print("readByte",hex(address),hex(data))
    return data & 0xFF

def readWord(address):
    data = 0
    for x in discovered_cards.keys():
        if not x.startswith("main_bus._"):
            data |= discovered_cards[x].readWord(address)
    #print("readWord",hex(address),hex(data))
    return data & 0xFFFF

def writeByte(address,value):
    #print("writeByte",hex(address),hex(value))
    for x in discovered_cards.keys():
        if not x.startswith("main_bus._"):
            discovered_cards[x].writeByte(address,value)

def writeWord(address,value):
    #print("writeWord",hex(address),hex(value))
    for x in discovered_cards.keys():
        if not x.startswith("main_bus._"):
            discovered_cards[x].writeWord(address,value)
        
def tick():
    for x in discovered_cards.keys():
        if not x.startswith("main_bus._"):
            discovered_cards[x].tick()
    
def checkINT():
    ints = []
    for x in discovered_cards.keys():
        if not x.startswith("main_bus._"):
            ints.extend(discovered_cards[x].checkINT())
    return ints
