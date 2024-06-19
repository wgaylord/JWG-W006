import backplane

class Registers:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.F = 0
        self.G = 0
        self.H = 0
        
        self.PRAS = 0
        self.PRBS = 0
        
        self.PORA = 0
        self.PORB = 0
        
        self.APA = 0
        self.APB = 0
        
        self.SP = 0
        
        self.RA = 0
        
    def debug(self):
        print("A:",self.A,"B:",self.B,"C:",self.C,"D:",self.D,"E:",self.E,"F:",self.F,"G:",self.G,"H:",self.H)
        print("PRAS:",self.PRAS,"PRBS:",self.PRBS,"PORA:",self.PORA,"PORB:",self.PORB,"APA:",self.APA,"APB:",self.APB)
        print("SP:",self.SP,"RA:",self.RA)
        
    
    
    def readWord(self,num):
        match num:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return self.A
            case 3:
                return self.B
            case 4:
                return self.C
            case 5:
                return self.D
            case 6:
                return self.E
            case 7:
                return self.F
            case 8:
                return self.G
            case 9:
                return self.H
            case _:
                print("Invalid register number for 16-bit read\n")
                return 0
       
    def writeWord(self,num,value):
        if num > 0xffff:
            num = 0xffff & num
        match num:
            case 0:
                pass
            case 1:
                pass
            case 2:
                self.A = value
            case 3:
                self.B = value
            case 4:
                self.C = value
            case 5:
                self.D = value
            case 6:
                self.E = value
            case 7:
                self.F = value
            case 8:
                self.G = value
            case 9:
                self.H = value
            case _:
                print("Invalid register number for 16-bit write\n")

    def readDWord(self,num):
        match num:
            case 2:
                return self.A + (self.B << 16)
            case 4:
                return self.C + (self.D << 16)
            case 6:
                return self.E + (self.F << 16)
            case 8:
                return self.G + (self.H << 16)
            case 10:
                return self.PRAS
            case 11:
                return self.PRBS
            case 12:
                return self.PORA
            case 13:  
                return self.PORB
            case 14:
                return self.APA
            case 15:
                return self.APB
            case 16:
                return self.SP
            case 17:
                return self.RA     
            case _:
                print("Invalid register number for 32-bit read\n")
                return 0
       
    def writeDWord(self,num,value):
        if num > 0xffffffff:
            num = 0xffffffff & num
        match num:
            case 2:
                self.A = value & 0xFFFF
                self.B = (value >> 16)
            case 4:
                self.C = value & 0xFFFF
                self.D = (value >> 16)
            case 6:
                self.E = value & 0xFFFF
                self.F = (value >> 16)
            case 8:
                self.G = value & 0xFFFF
                self.H = (value >> 16)
            case 10:
                self.PRAS = value
                self.updateAPR()
            case 11:
                self.PRBS = value
                self.updateAPR()
            case 12:
                self.PORA = value
                self.updateAPR()
            case 13:  
                self.PORB = value
                self.updateAPR()
            case 16:
                self.SP = value
            case 17:
                self.RA = value
            case _:
                print("Invalid register number for 32-bit write\n")

    def updateAPR(self):
        self.APA = self.PRAS + self.PORA
        self.APB = self.PRBS + self.PORB

class MMU:
    
    enabled = False
    
    PTI = 0
    
    def __init__(self):
        pass
        
    def readByte(self,address):
        if not self.enabled:
            return backplane.readByte(address)

    def readWord(self,address):
        if not self.enabled:
            return backplane.readWord(address)

    def writeByte(self,address,value):
        if not self.enabled:
            backplane.writeByte(address,value)

    def writeWord(self,address,value):
        if not self.enabled:
            backplane.writeWord(address,value)


class Flags:
    def __init__(self):
        self.carry = False
        self.zero = False
        self.greater = False
        self.equal = False

    def getValue(self):
        return self.carry + (self.zero * 2) + (self.greater * 4) + (self.equal * 8)

    def setValue(self,value):
        self.carry = value & 1 == 1
        self.zero = value & 2 == 2
        self.greater = value & 4 == 4
        self.equal = value & 8 == 8 

class Status:
    def __init__(self):
        self.supervisor = True

    def getValue(self):
        return self.supervisor

    def setValue(self,value):
        self.supervisor = value & 1 == 1

class cpu:
    
    PC = 0
    
    IVT = 0
   
    mmu = None
    
    registers = None
    
    flags = None
    
    status = None
        
    def __init__(self):
        pass
        
    def init(self):
        self.mmu = MMU()
        self.registers = Registers()
        self.flags = Flags()
        self.status = Status()
        
    def tick(self):
        
        opcodePart1 = self.mmu.readWord(self.PC)
        self.PC += 2
        opcodePart2 = self.mmu.readWord(self.PC)
        self.PC += 2

        opcode = (opcodePart1 & 0xFF)
        A = (opcodePart1 & 0xFF00) >> 8
        B = (opcodePart2 & 0xFF)
        C = (opcodePart2 & 0xFF00) >> 8
               
        #print("OPCODE:",hex(opcode),"A:",hex(A),"B:",hex(B),"C:",hex(C))
               
        match opcode:
            case 0:
                return
            case 1:
                val = self.registers.readWord(A) + self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 2:
                val = self.registers.readDWord(A) + self.registers.readDWord(B)
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
            case 3:
                val = self.registers.readWord(A) - self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 4:
                val = self.registers.readDWord(A) - self.registers.readDWord(B)
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
            case 5:
                val = self.registers.readWord(A) * self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 6:
                val = self.registers.readDWord(A) * self.registers.readDWord(B)
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
            case 7:
                val = self.registers.readWord(A) // self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 8:
                val = self.registers.readDWord(A) // self.registers.readDWord(B)
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
            case 9:
                val = self.registers.readWord(A) % self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 10:
                val = self.registers.readDWord(A) % self.registers.readDWord(B)
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
            case 11:
                val = self.registers.readWord(A) | self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(val & 0xFFFF)
            case 12:
                val = self.registers.readDWord(A) | self.registers.readDWord(B)
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
            case 13:
                val = self.registers.readWord(A) & self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 14:
                val = self.registers.readDWord(A) & self.registers.readDWord(B)
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
                
            case 15:
                val = self.registers.readWord(A) ^ self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 16:
                val = self.registers.readDWord(A) ^ self.registers.readDWord(B)
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
                
            case 17:
                val = self.registers.readWord(A)
                
                val = val << 1
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 18:
                val = self.registers.readDWord(A)
                
                val = val << 1
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
                
            case 19:
                val = self.registers.readWord(A)
                
                val = val >> 1
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 20:
                val = self.registers.readDWord(A)
                
                val = val >> 1
                
                if val != val & 0xFFFFFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(C,val & 0xFFFFFFFF)
                
            case 21:
                val = self.registers.readWord(A)
                
                val = (~val) & 0xFFFF
                
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 22:
                val = self.registers.readDWord(A)
                
                val = (~val) & 0xFFFFFFFF

                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(val & 0xFFFFFFFF)
                
            case 23:
                vala = self.registers.readWord(A)
                valb = self.registers.readWord(B)
                
                if vala > valb:
                    self.flags.greater = True
                    self.flags.equal = False
                elif vala == valb:
                    self.flags.greater = False
                    self.flags.equal = True
                else:
                    self.flags.equal = False
                    self.flags.greater = False
            case 24:
                vala = self.registers.readDWord(A)
                valb = self.registers.readDWord(B)
                
                if vala > valb:
                    self.flags.greater = True
                    self.flags.equal = False
                elif vala == valb:
                    self.flags.greater = False
                    self.flags.equal = True
                else:
                    self.flags.equal = False
                    self.flags.greater = False 
                    
            case 25:
                sp = self.registers.readDWord(16)
                
                val = self.registers.readWord(A) & 0xF
                
                self.mmu.writeByte(sp,val)
                
                self.registers.writeDWord(16,sp+1)
               
            case 26:
                sp = self.registers.readDWord(16)
                
                val = self.registers.readWord(A)
                
                self.mmu.writeWord(sp,val)
                
                self.registers.writeDWord(16,sp+2) 
            case 27:
                sp = self.registers.readDWord(16)
                
                val = self.registers.readDWord(A)
                
                self.mmu.writeDWord(sp,val&0xFFFF)
                self.mmu.writeDWord(sp+2,val>>16)
                
                self.registers.writeDWord(16,sp+4) 
                
            case 28:
                sp = self.registers.readDWord(16)
                
                self.registers.writeByte(C,self.mmu.readByte(sp-1,val))
                
                self.registers.writeDWord(16,sp-1)
               
            case 29:
                ssp = self.registers.readDWord(16)
                
                self.registers.writeWord(C,self.mmu.readWord(sp-2,val))
                
                self.registers.writeDWord(16,sp-2)
            case 30:
                sp = self.registers.readDWord(16)
                
                part1 = self.mmu.readWord(sp-2,val)
                part2 = self.mmu.readWord(sp-4,val)
                
                
                val = part1<<16 + part2
                
                self.registers.writeDWord(C,val)
                
                self.registers.writeDWord(16,sp-4) 
                
                
            case 31:
                addr = self.mmu.readDWord(self.PC) << 16
                self.PC += 2
                addr += self.mmu.readDWord(self.PC)
                self.PC += 2
            
                if A & 1 == 1 and self.flags.carry:
                    self.PC = addr
                if A & 2 == 2 and self.flags.zero:
                    self.PC = addr
                if A & 4 == 4 and self.flags.greater:
                    self.PC = addr
                if A & 8 == 8 and self.flags.equal:
                    self.PC = addr

            case 32:
                addr = self.registers.readDWord(B)
                
                if A & 1 == 1 and self.flags.carry:
                    self.PC = addr
                if A & 2 == 2 and self.flags.zero:
                    self.PC = addr
                if A & 4 == 4 and self.flags.greater:
                    self.PC = addr
                if A & 8 == 8 and self.flags.equal:
                    self.PC = addr

            case 33:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC = addr

            case 34:
                addr = self.registers.readDWord(B)
                self.PC = addr
                
            case 35:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.reaDWord(self.PC)<< 16
                self.registers.writeDWord(17,self.PC + 2)
                self.PC = addr

            case 36:
                addr = self.registers.readDWord(B)
                self.registers.writeDWord(17,self.PC)
                self.PC = addr
                
            case 37:
                data = self.mmu.readWord(self.PC)
                self.PC += 4
                self.registers.writeWord(C,data)
                
            case 38:
                data = self.mmu.readWord(self.PC)
                self.PC += 2
                data += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                self.registers.writeDWord(C,ata)

            case 39:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                data = self.mmu.readByte(addr)
                
                self.registers.writeWord(C,data)
            case 40:
                addr = self.mmu.readWord(self.PC) << 16
                self.PC += 2
                addr += self.mmu.readWord(self.PC)
                self.PC += 2
                
                data = self.mmu.readWord(addr)
                
                self.registers.writeWord(C,data)
            case 41:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                data = self.mmu.readWord(addr)
                data += self.mmu.readWord(addr+2) << 16
                
                self.registers.writeDWord(C,data)
                
            case 42:
                addr = self.registers.readDWord(B)
                
                data = self.mmu.readByte(addr)
                
                self.registers.writeWord(C,data)
            case 43:
                addr = self.registers.readDWord(B)
                
                data = self.mmu.readWord(addr)
                
                self.registers.writeWord(C,data)
            case 44:
                addr = self.registers.readDWord(B)
                
                data = self.mmu.readWord(addr)
                data += self.mmu.readWord(addr+2) << 16
                
                self.registers.writeDWord(C,data)  
                
            case 45:
                self.registers.writeWord(C,self.flags.getValue())
                
            case 46:
                self.registers.writeWord(C,self.status.getValue())
                
            case 47:
                addr = self.mmu.readWord(self.PC) 
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                self.mmu.writeByte(addr,self.registers.readWord(A)&0xFF)
                
            case 48:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                self.mmu.writeWord(addr,self.registers.readWord(A))
            case 49:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                data = self.registers.readDWord(A)
                
                self.mmu.writeWord(addr,data&0xFFFF)
                self.mmu.writeWord(addr+2,data>>16)  
                
            case 50:
                addr = self.registers.readDWord(B)
                
                self.mmu.writeByte(addr,self.registers.readWord(A)&0xFF)
            case 51:
                addr = self.registers.readDWord(B)
               
                self.mmu.writeWord(addr,self.registers.readWord(A))
            case 52:
                addr = self.registers.readDWord(B)
                
                self.mmu.writeWord(addr,data&0xFFFF)
                self.mmu.writeWord(addr+2,data>>16)  
            case 53:
                self.flags.setValue(self.registers.readWord(A))
                
            case 54:
                print("INTTRUPT ABS NOT IMPLEMENTED!")
            case 55:
                print("INTTRUPT REG NOT IMPLEMENTED!")
            
            
            case 64:
                if self.status.supervisor:
                    pass   
                
            case 65:
                if self.status.supervisor:
                    self.status.setValue(self.registers.readWord(A))
            case 66:
                if self.status.supervisor:
                    self.registers.writeDWord(C,self.PTI)
                    
            case 67:
                if self.status.supervisor:
                    self.PTI = self.registers.readDWord(A)
                    
            case 68:
                if self.status.supervisor:
                    self.registers.writeDWord(C,self.IVT)
                    
            case 69:
                if self.status.supervisor:
                    self.IVT = self.registers.readDWord(A)
                
            case 70:
                if self.status.supervisor:
                    print("Intteurpt Return not implemented")
                    
            case 255:
                print("HALTED")
                self.PC = -1
