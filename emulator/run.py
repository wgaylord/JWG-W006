import backplane
import cpu
import time
import sys

print("Initalizing Emulator.")
print("=====================")

print("  Initalizing Backplane.")
print("  ======================")
backplane.init()

cpu = cpu.cpu()


print("  Initalizing CPU.")
cpu.init()
print("  CPU Initalized. starting emulator.")
sys.stdout.write('\r')
sys.stdout.flush()



while True:
    #time.sleep(0.0001)
    #print("PC:",hex(cpu.PC))
    #cpu.registers.debug()
    #for x in range(32):
    #print(backplane.readByte(cpu.registers.APB))
    #print("")
    #print("========================================")
    cpu.tick()
    
    if cpu.PC == -1:
        break
