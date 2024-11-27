import json

from pprint import pprint

data = json.loads(open("out.i").read())

program = data["program"]
types = data["types"]

opcodes = ["JUMP_ABS __init__"]

functions = {}

# Registers AB CD used for all input args 
# Register EF used for returns

registers16 = {"E":{"name":"","count":0},"F":{"name":"","count":0},"G":{"name":"","count":0},"H":{"name":"","count":0}}
registers32 = {"EF":{"name":"","count":0},"GH":{"name":"","count":0}}

registerOverlap16 = {"A":"AB","B":"AB","C":"CD","D":"CD","E":"EF","F":"EF","G":"GH","H":"GH"}
registerOverlap32 = {"AB":["A","B"],"CD":["C","D"],"EF":["E","F"],"GH":["G","H"]}

variables = {}

argCount = 0

registerArgs = ["A","B","C","D"]
registerArgs32 = ["AB","AB","CD","CD"]

global_vars = {}
stackOffset = 0

def sortCount16(x):
    return registers16[x]["count"]

def sortCount32(x):
    return registers32[x]["count"]

def GetRegister16():
    for x in registers16.keys():
        if registers16[x]["count"] == 0:
            return x
    
    keys = list(registers16.keys())
    keys.sort(reverse=True, key=sortCount16)
    print(keys)
    
    
    pass
    
    
def GetRegister32():
    for x in registers32.keys():
        if registers32[x]["count"] == 0:
            return x
    
    keys = list(registers32.keys())
    keys.sort(reverse=True, key=sortCount32)
    print(keys)
    
    
    pass
    
def SetRegister16InUse(x,name):
    registers16[x]["name"] = name
    registers16[x]["count"] = 1
    registers32[registerOverlap16[x]]["count"] = 1
    
def SetRegister32InUse(x,name):
    registers32[x]["name"] = name
    registers32[x]["count"] = 1
    for y in registerOverlap32[x]:
        registers16[y]["count"] = 1
  
def SetRegister32Free(x,name):
    registers32[x]["name"] = ""
    registers32[x]["count"] = 0
    for y in registerOverlap32[x]:
        registers16[y]["count"] = 0
  
def SetRegister16Free(x,name):
    registers16[x]["name"] = ""
    registers16[x]["count"] = 0
    registers32[registerOverlap16[x]]["count"] = 0

def isInRegister16(name):
    for x in registers16.keys():
        if registers16[x]["name"] == name:
            return x
    return None
    
def isInRegister32(name):
    for x in registers32.keys():
        if registers32[x]["name"] == name:
            return x
    return None

def regCountUpdate(name):
    for x in registers16.keys():
        if registers16[x]["name"] == name:
            registers16[x]["count"] += 1
            registers32[registerOverlap16[x]]["count"] += 1
    
    for x in registers32.keys():
        if registers32[x]["name"] == name:
            registers32[x]["count"] += 1
            for y in registerOverlap32[x]:
                registers16[y]["count"] += 1
    
def walk(prog):
    global variables
    global global_vars
    global opcodes
    global stackOffset
    global argCount
    
    for x in prog:
        #print("variables")
        #pprint(variables)
        #print("Register Coloring")
        #print("===============================================================")
        #pprint(registers16)
        #pprint(registers32)
        #print("===============================================================")
        if x[0] == "callFunc":
            opcodes.append(";"+str(x))
            opcodes.append("; Byte Arg Count "+str(argCount))
            opcodes.append("CALL_ABS "+x[1])

            if argCount > 2:
                opcodes.append("PUSHd CD")
            if argCount > 0:
                opcodes.append("POPd AB")
            argCount = 0

        elif x[0] == "defVar":
            if x[1]["local"]:
                #opcodes.append(";"+str(x))
                variables[x[1]["name"]] = x[1]
                variables[x[1]["name"]]["register"] = None
                variables[x[1]["name"]]["stack"] = stackOffset
                stackOffset += types[x[1]["type"]]["size"]
                size = types[x[1]["type"]]["size"]
                variables[x[1]["name"]]["size"] = size
                if size == 1:
                    opcodes.append("PUSHb ZERO")
                elif size == 2:
                    opcodes.append("PUSHw ZERO")
                elif size == 4:
                    opcodes.append("PUSHd ZERO")
            else:
                global_vars[x[1]["name"]] = x[1]
                global_vars[x[1]["name"]]["size"] = types[x[1]["type"]]["size"]
                global_vars[x[1]["name"]]["register"] = None
                global_vars[x[1]["name"]]["addr"] = x[1]["name"]
            
        elif x[0] == "funcDef":
            opcodes.append(";"+str(x))
        
            count = 0
        
            for z in x[2]:
                variables[z["name"]] = z
                variables[z["name"]]["size"] = types[z["type"]]["size"]
                if types[z["type"]]["size"] < 3:
                    variables[z["name"]]["register"] = registerArgs[count]
                    count += 1
                if types[z["type"]]["size"] == 4:
                    variables[z["name"]]["register"] = registerArgs32[count]
                    count += 2
        
            for z in global_vars.keys():
                variables[z] = global_vars[z]
        
            opcodes.append(x[1]+":")
            opcodes.append("PUSHd RA")
            opcodes.append("PUSHd PRAS")
            opcodes.append("PUSHd PORA")
            opcodes.append("ORd SP, ZERO, PRAS")
            opcodes.append("ORd ZERO, ZERO, PORA")
            
        elif x[0] == "loadVar":
            print("loadVar found check compiler!")
            #exit()
        elif x[0] == "loadVarAsArg":
            opcodes.append(";"+str(x))
            if argCount == 0:
                opcodes.append("PUSHd AB")
            elif argCount == 2:
                opcodes.append("PUSHd CD")
            t = """
            if variables[x[1]]["size"] < 3:
                if variables[x[1]]["register"] == None:
                    reg = GetRegister16()
                    if variables[x[1]]["local"]:
                        opcodes.append("LOADw_imd PORA, "+str(variables[x[1]]["stack"]))
                        opcodes.append("LOADw_indirect "+reg+", APA")
                        SetRegister16InUse(reg,x[1])
                    else:
                        opcodes.append("LOADw "+reg+", "+variables[x[1]]["addr"])
                        SetRegister16InUse(reg,x[1])
            if variables[x[1]]["size"] == 4:
                if variables[x[1]]["register"] == None:
                    reg = GetRegister32()
                    if variables[x[1]]["local"]:
                        opcodes.append("LOADd_imd PORA, "+str(variables[x[1]]["stack"]))
                        opcodes.append("LOADd_indirect "+reg+", APA"+"; "+str(x))
                        SetRegister32InUse(reg,x[1])
                    else:
                        opcodes.append("LOADd "+reg+", "+variables[x[1]]["addr"])
                        SetRegister32InUse(reg,x[1])"""
                        
                        
            if variables[x[1]]["size"] == 4:
                reg =  isInRegister32(x[1])
                if reg:
                    regCountUpdate(reg)
                    opcodes.append("ORd ZERO, "+reg+", "+registerArgs32[argCount])
                else:
                    reg = GetRegister32()
                    if variables[x[1]]["local"]:
                        opcodes.append("LOADd_imd PORA, "+str(variables[x[1]]["stack"]))
                        opcodes.append("LOADd_indirect "+reg+", APA"+"; "+str(x))
                        opcodes.append("ORd ZERO, "+reg+", "+registerArgs32[argCount])
                        SetRegister32InUse(reg,x[1])
                    else:
                        opcodes.append("LOADd "+reg+", "+variables[x[1]]["addr"])
                        opcodes.append("ORd ZERO, "+reg+", "+registerArgs32[argCount])
                        SetRegister32InUse(reg,x[1])
                argCount += 2
            if variables[x[1]]["size"] == 2:
                reg =  isInRegister16(x[1])
                if reg:
                    regCountUpdate(reg)
                    opcodes.append("ORw ZERO, "+reg+", "+registerArgs16[argCount])
                else:
                    reg = GetRegister16()
                    if variables[x[1]]["local"]:
                        opcodes.append("LOADd_imd PORA, "+str(variables[x[1]]["stack"]))
                        opcodes.append("LOADw_indirect "+reg+", APA"+"; "+str(x))
                        opcodes.append("ORw ZERO, "+reg+", "+registerArgs32[argCount])
                        SetRegister16InUse(reg,x[1])
                    else:
                        opcodes.append("LOADw "+reg+", "+variables[x[1]]["addr"])
                        opcodes.append("ORw ZERO, "+reg+", "+registerArgs32[argCount])
                        SetRegister16InUse(reg,x[1]) 
                argCount += 1
                        
            if variables[x[1]]["size"] == 1:
                reg =  isInRegister16(x[1])
                if reg:
                    regCountUpdate(reg)
                    opcodes.append("ORw ZERO, "+reg+", "+registerArgs16[argCount])
                else:
                    reg = GetRegister16()
                    if variables[x[1]]["local"]:
                        opcodes.append("LOADd_imd PORA, "+str(variables[x[1]]["stack"]))
                        opcodes.append("LOADb_indirect "+reg+", APA"+"; "+str(x))
                        opcodes.append("ORw ZERO, "+reg+", "+registerArgs32[argCount])
                        SetRegister16InUse(reg,x[1])
                    else:
                        opcodes.append("LOADd "+reg+", "+variables[x[1]]["addr"])
                        opcodes.append("ORw ZERO, "+reg+", "+registerArgs32[argCount])
                        SetRegister16InUse(reg,x[1])
                argCount += 1
                
            pass
        elif x[0] == "loadConstAsArg":
            opcodes.append(";"+str(x))
            pass
        elif x[0] == "setArg":
            print("setArg found check compiler!")
            exit()
        elif x[0] == "arrayAccess":
            opcodes.append(";"+str(x))
        elif x[0] == "binOpLeft":
            opcodes.append(";"+str(x))
        elif x[0] == "binOpRight":
            opcodes.append(";"+str(x))
        elif x[0] == "binOp":
            opcodes.append(";"+str(x))
        elif x[0] == "loadConst":
            opcodes.append(";"+str(x))
        elif x[0] == "while":
            opcodes.append(";"+str(x))
        elif x[0] == "assign":
            opcodes.append(";"+str(x))
        elif x[0] == "while_end":
            opcodes.append(";"+str(x))
        elif x[0] == "return":
            opcodes.append(";"+str(x))
            opcodes.append("POPd PORA")
            opcodes.append("POPd PRAS")
            opcodes.append("POPd RA ")
            opcodes.append("JUMP_REG RA")
            variables = {}
            stackOffset = 0

walk(program)


def walkGlobalInit(prog,name):
    for x in prog:
        if x[0] == "loadConst":
            if global_vars[name]["size"] == 4:
                opcodes.append("LOADd_imd AB, "+str(x[1]))
                opcodes.append("STOREd AB, "+name)
            if global_vars[name]["size"] == 2:
                opcodes.append("LOADw_imd A, "+str(x[1]))
                opcodes.append("STOREw A, "+name)
            if global_vars[name]["size"] == 1:
                opcodes.append("LOADw_imd A, "+str(x[1]))
                opcodes.append("STOREb A, "+name)

opcodes.append("__init__:")
for x in global_vars:
    walkGlobalInit(global_vars[x]["init"],x)

opcodes.append("LOADd_imd AB, 0")
opcodes.append("LOADd_imd SP, stack")
opcodes.append("JUMP_ABS main")
opcodes.append("#addr 0x4fff")

for x in global_vars:
    opcodes.append(x+":")
    opcodes.append("#d 00`"+str(8*global_vars[x]["size"]))
    
opcodes.append("stack:")



#pprint(global_vars)
#pprint(opcodes)

asm = ""

q = open("test.asm","w+")
for x in opcodes:
    asm += x+"\n"
q.write(asm)  
q.close()
