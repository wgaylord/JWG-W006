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
        self.I = 0
        self.J = 0
        self.K = 0
        self.L = 0
        self.M = 0
        self.N = 0
        
        
        self.PRAS = 0
        self.PRBS = 0
        
        self.PORA = 0
        self.PORB = 0
        
        self.APA = 0
        self.APB = 0
        
        self.SP = 0
        
        self.RA = 0
        
        self.IR = 0
        
    def debug(self):
        print("A:",self.A,"B:",self.B,"C:",self.C,"D:",self.D,"E:",self.E,"F:",self.F,"G:",self.G)
        print("H:",self.H,"I:",self.I,"J:",self.J,"K:",self.K,"L:",self.L,"M:",self.M,"N:",self.N)
        print("PRAS:",self.PRAS,"PRBS:",self.PRBS,"PORA:",self.PORA,"PORB:",self.PORB,"APA:",self.APA,"APB:",self.APB)
        print("SP:",self.SP,"RA:",hex(self.RA),"IR:",hex(self.IR))
        
    
    
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
            case 10:
                return self.I
            case 11:
                return self.J
            case 12:
                return self.K
            case 13:
                return self.L
            case 14:
                return self.M
            case 15:
                return self.N
            case _:
                print("Invalid register number for 16-bit read\n",num)
                return 0
       
    def writeWord(self,num,value):
        if value > 0xffff:
            value = 0xffff & value
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
            case 10:
                self.I = value
            case 11:
                self.J  = value
            case 12:
                self.K = value
            case 13:
                self.L = value
            case 14:
                self.M = value
            case 15:
                self.N = value
            case _:
                print("Invalid register number for 16-bit write\n",num)

    def readDWord(self,num):
        match num:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return self.A + (self.B << 16)
            case 4:
                return self.C + (self.D << 16)
            case 6:
                return self.E + (self.F << 16)
            case 8:
                return self.G + (self.H << 16)
            case 10:
                return self.I + (self.J << 16)
            case 12:
                return self.K + (self.L << 16)
            case 14:
                return self.M + (self.N << 16)
            case 16:
                return self.PRAS
            case 17:
                return self.PRBS
            case 18:
                return self.PORA
            case 19:  
                return self.PORB
            case 20:
                return self.APA
            case 21:
                return self.APB
            case 22:
                return self.SP
            case 23:
                return self.RA    
            case 24:
                return self.IR 
            case _:
                print("Invalid register number for 32-bit read\n",num)
                return 0
       
    def writeDWord(self,num,value):
        if value > 0xffffffff:
            value = 0xffffffff & num
        match num:
            case 0:
                pass
            case 1:
                pass
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
                self.I = value & 0xFFFF
                self.J = (value >> 16)
            case 12:
                self.K = value & 0xFFFF
                self.L = (value >> 16)
            case 14:
                self.M = value & 0xFFFF
                self.N = (value >> 16)
            case 16:
                self.PRAS = value
                self.updateAPR()
            case 17:
                self.PRBS = value
                self.updateAPR()
            case 18:
                self.PORA = value
                self.updateAPR()
            case 19:  
                self.PORB = value
                self.updateAPR()
            case 20:
                pass
            case 21:
                pass
            case 22:
                self.SP = value
            case 23:
                self.RA = value
            case 24:
                self.IR = value
            case _:
                print("Invalid register number for 32-bit write\n",num)

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
        self.interrupts_enabled = False
        self.in_int = False
        self.int_enable_previous = False
        self.supervisor_previous = True

    def getValue(self):
        return self.supervisor + (self.interrupts_enabled * 2) + (self.in_int * 4) + (self.int_enable_previous * 8) + (self.supervisor_previous * 16)

    def setValue(self,value):
        self.supervisor = value & 1 == 1
        self.interrupts_enabled = value & 2 == 2
        self.in_int = value & 4 == 4
        self.int_enable_previous = value & 8 == 8
        self.supervisor_previous = value & 16 == 16

    def debug(self):
        print("SUP:",self.supervisor,"INTS:",self.interrupts_enabled,"IN_INT:",self.in_int)

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
        
        
    def do_interrupt(self,num):
        if self.status.interrupts_enabled and not self.status.in_int:
            #print("INT",num)
            self.status.supervisor_previous = self.status.supervisor
            self.status.supervisor = True
            
            self.status.int_enable_previous = self.status.interrupts_enabled
            self.status.interrupts_enabled = False
        
            self.registers.IR = self.PC
            
        
            int_addr = self.IVT + (num*4)
            
            #print(hex(int_addr))
            
            addr = self.mmu.readWord(int_addr)
            addr = addr | (self.mmu.readWord(int_addr + 2) << 16)
           
            self.PC = addr
            self.int_count = 0
            self.status.in_int = True
        
    def return_interrupt(self):
        #print(self.status.interrupts_enabled,self.status.in_int)
        if self.status.in_int:
            self.status.supervisor = self.status.supervisor_previous
            self.status.interrupts_enabled = self.status.int_enable_previous
            
            self.PC = self.registers.IR
            
            self.status.in_int = False
        
    def tick(self):
        if self.status.interrupts_enabled:
            interrupt = backplane.checkINT()
            if len(interrupt) > 0:
                self.do_interrupt(interrupt[0])
        
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
            case 0x00:
                return
            case 0x01:
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
            case 0x02:
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
            case 0x03:
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
            case 0x04:
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
            case 0x05:
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
            case 0x06:
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
            case 0x07:
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
            case 0x08:
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
            case 0x09:
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
            case 0x0A:
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
            case 0x0B:
                val = self.registers.readWord(A) | self.registers.readWord(B)
                
                if val != val & 0xFFFF:
                    self.flags.carry = True
                else:
                    self.flags.carry = False
                    
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 0x0C:
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
            case 0x0D:
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
            case 0x0E:
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
                
            case 0x0F:
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
            case 0x10:
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
                
            case 0x11:
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
            case 0x12:
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
                
            case 0x13:
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
            case 0x14:
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
                
            case 0x15:
                val = self.registers.readWord(A)
                
                val = (~val) & 0xFFFF
                
                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeWord(C,val & 0xFFFF)
            case 0x16:
                val = self.registers.readDWord(A)
                
                val = (~val) & 0xFFFFFFFF

                if val == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                    
                self.registers.writeDWord(val & 0xFFFFFFFF)
                
            case 0x17:
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
            case 0x18:
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
                    
            case 0x19:
                sp = self.registers.readDWord(22)
                
                val = self.registers.readWord(A) & 0xF
                
                self.mmu.writeByte(sp,val)
                
                self.registers.writeDWord(22,sp+1)
               
            case 0x1A:
                sp = self.registers.readDWord(22)
                
                val = self.registers.readWord(A)
                
                self.mmu.writeWord(sp,val)
                
                self.registers.writeDWord(22,sp+2) 
            case 0x1B:
                sp = self.registers.readDWord(22)
                
                val = self.registers.readDWord(A)
                self.mmu.writeWord(sp,val&0xFFFF)
                self.mmu.writeWord(sp+2,val>>16)
                
                
                
                self.registers.writeDWord(22,sp+4) 
                
            case 0x1C:
                sp = self.registers.readDWord(22)
                
                self.registers.writeWord(C,self.mmu.readByte(sp-1))
                
                self.registers.writeDWord(22,sp-1)
               
            case 0x1D:
                sp = self.registers.readDWord(22)
                #print(hex(self.mmu.readWord(sp)))
                #print(hex(self.mmu.readWord(sp-2)))
                #print(hex(self.mmu.readWord(sp-4)))
                self.registers.writeWord(C,self.mmu.readWord(sp-2))
                
                self.registers.writeDWord(22,sp-2)
            case 0x1E:
                sp = self.registers.readDWord(22)
                
                part1 = self.mmu.readWord(sp-2)
                part2 = self.mmu.readWord(sp-4)
                
                val = (part1<<16) + part2
                
                
                self.registers.writeDWord(C,val)
                
                self.registers.writeDWord(22,sp-4) 
                
                
            case 0x1F:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
            
                if A & 1 == 1 and self.flags.carry:
                    self.PC = addr
                if A & 2 == 2 and self.flags.zero:
                    self.PC = addr
                if A & 4 == 4 and self.flags.greater:
                    self.PC = addr
                if A & 8 == 8 and self.flags.equal:
                    self.PC = addr

            case 0x20:
                addr = self.registers.readDWord(B)
                
                if A & 1 == 1 and self.flags.carry:
                    self.PC = addr
                if A & 2 == 2 and self.flags.zero:
                    self.PC = addr
                if A & 4 == 4 and self.flags.greater:
                    self.PC = addr
                if A & 8 == 8 and self.flags.equal:
                    self.PC = addr

            case 0x21:
 
                addr = self.mmu.readWord(self.PC)             
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC = addr

            case 0x22:
                addr = self.registers.readDWord(B)
                self.PC = addr
                
            case 0x23:

                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.registers.writeDWord(23,self.PC + 2)
                self.PC = addr

            case 0x24:
                addr = self.registers.readDWord(B)
                self.registers.writeDWord(23,self.PC)
                self.PC = addr
                
            case 0x25:
                data = self.mmu.readWord(self.PC)
                self.PC += 4
                self.registers.writeWord(C,data)
                if data == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                
            case 0x26:
                data = self.mmu.readWord(self.PC)
                self.PC += 2
                data += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                self.registers.writeDWord(C,data)
                if data == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False

            case 0x27:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                data = self.mmu.readByte(addr)
                
                self.registers.writeWord(C,data)
                if data == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
            case 0x28:
                addr = self.mmu.readWord(self.PC) << 16
                self.PC += 2
                addr += self.mmu.readWord(self.PC)
                self.PC += 2
                
                data = self.mmu.readWord(addr)
                
                self.registers.writeWord(C,data)
                if data == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
            case 0x29:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                data = self.mmu.readWord(addr)
                data += self.mmu.readWord(addr+2) << 16
                
                self.registers.writeDWord(C,data)
                if data == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                
            case 0x2A:
                
                addr = self.registers.readDWord(B)
                
                data = self.mmu.readByte(addr)
                
                self.registers.writeWord(C,data)

                if data == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
            case 0x2B:
                addr = self.registers.readDWord(B)
                
                data = self.mmu.readWord(addr)
                
                self.registers.writeWord(C,data)
                if data == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
            case 0x2C:
                addr = self.registers.readDWord(B)
                
                data = self.mmu.readWord(addr)
                data += self.mmu.readWord(addr+2) << 16
                
                self.registers.writeDWord(C,data)  
                if data == 0:
                    self.flags.zero = True
                else:
                    self.flags.zero = False
                
            case 0x2D:
                self.registers.writeWord(C,self.flags.getValue())
                
            case 0x2E:
                self.registers.writeWord(C,self.status.getValue())
                
            case 0x2F:
                addr = self.mmu.readWord(self.PC) 
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                self.mmu.writeByte(addr,self.registers.readWord(A)&0xFF)
                
            case 0x30:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                self.mmu.writeWord(addr,self.registers.readWord(A))
            case 0x31:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                data = self.registers.readDWord(A)
                
                self.mmu.writeWord(addr,data&0xFFFF)
                self.mmu.writeWord(addr+2,data>>16)  
                
            case 0x32:
                addr = self.registers.readDWord(A)
                
                self.mmu.writeByte(addr,self.registers.readWord(B)&0xFF)
            case 0x33:
                addr = self.registers.readDWord(A)
               
                self.mmu.writeWord(addr,self.registers.readWord(B))
            case 0x34:
                addr = self.registers.readDWord(A)
                data = self.registers.readDWord(B)
                self.mmu.writeWord(addr,data&0xFFFF)
                self.mmu.writeWord(addr+2,data>>16)  
            case 0x35:
                self.flags.setValue(self.registers.readWord(A))
                
            case 0x36:
                self.do_interrupt(A)
            case 0x37:
                self.do_interrupt(self.registers.readWord(A))
            
            case 0x38:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                data = self.mmu.readByte(addr)
                
                self.registers.writeWord(C,data)
                data = self.registers.readWord(A)
                self.mmu.writeByte(addr,data)
            
            case 0x39:
                addr = self.mmu.readWord(self.PC)
                self.PC += 2
                addr += self.mmu.readWord(self.PC) << 16
                self.PC += 2
                
                data = self.mmu.readWord(addr)
                
                self.registers.writeWord(C,data)
                data = self.registers.readWord(A)
                
                self.mmu.writeWord(addr,data)
                
            case 0x40:
                addr = self.registers.readDWord(B)
                
                data = self.mmu.readByte(addr)
                
                self.registers.writeWord(C,data)
                data = self.registers.readWord(A)
                self.mmu.writeByte(addr,data)
            
            case 0x41:
                addr = self.registers.readDWord(B)
                
                data = self.mmu.readWord(addr)
                
                self.registers.writeWord(C,data)
                data = self.registers.readWord(A)
                
                self.mmu.writeWord(addr,data)
                
            
            case 0x80:
                if self.status.supervisor:
                    pass   
                
            case 0x81:
                if self.status.supervisor:
                    self.status.setValue(self.registers.readWord(A))
            case 0x82:
                if self.status.supervisor:
                    self.registers.writeDWord(C,self.PTI)
                    
            case 0x83:
                if self.status.supervisor:
                    self.PTI = self.registers.readDWord(A)
                    
            case 0x84:
                if self.status.supervisor:
                    self.registers.writeDWord(C,self.IVT)
                    
            case 0x85:
                if self.status.supervisor:
                    self.IVT = self.registers.readDWord(A)
                
            case 0x86:
                if self.status.supervisor:
                    self.return_interrupt()
            case 0x87:
                if self.status.supervisor:
                    self.status.interrupts_enabled = False
            case 0x88:
                if self.status.supervisor:
                    self.status.interrupts_enabled = True
                    
            case 0xff:
                print("HALTED")
                self.PC = -1
