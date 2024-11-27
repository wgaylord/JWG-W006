#once
#include "cpu_def.asm"


SERIAL_DATA = 0xC0000000
SERIAL_BUFFERED = 0xC0000001
SERIAL_SETTINGS = 0xC0000003

SERIAL_INT_SETTINGS_HAS_DATA =1
SERIAL_INT_SETTINGS_BUFFER_FULL = 2
SERIAL_INT_SETTINGS_DID_WRITE = 4

JUMP_ABS BUFFERED_SERIAL_END


SerialGetChar:
    LOADb A, SERIAL_BUFFERED
    CMPw A, ZERO
    BRH_ABS EQUAL, SerialGetChar
    LOADb N, SERIAL_DATA
    RTN
    
SerialWriteChar:
    STOREb A, SERIAL_DATA
    RTN


SerialWriteDWord:
    PUSHd RA
    PUSHd PRBS
    PUSHd PORB
    PUSHd CD
    PUSHd GH
    PUSHd EF
    LOADd_imd PRBS, 0x400
    LOADd_imd PORB, 32
    STOREb_indirect APB, ZERO
    SUBd PORB, ONE, PORB
    ORd APA, ZERO, IJ
    LOADd_imd CD, 10
    LOADd_imd GH, 0x30
    SerialWriteDWord_LOOP:
    REMd AB, CD, EF
    DIVd AB, CD, AB
    ADDd EF, GH, EF
    STOREb_indirect APB, E
    SUBd PORB, ONE, PORB
    CMPd AB, ZERO
    BRH_ABS EQUAL, SerialWriteDWord_EXIT
    JUMP_ABS SerialWriteDWord_LOOP
    SerialWriteDWord_EXIT:
    ADDd APB, ONE, AB
    CALL_ABS SerialPrintString
    POPd EF
    POPd GH
    POPd CD
    POPd PORB
    POPd PRBS
    POPd RA
    RTN

SerialPrintString:
    ; AB contains a pointer to the Null terminated String
    PUSHd PRAS
    PUSHd PORA
    
    ORd AB, AB, PRAS
    LOADw_imd A, 13
    LOADw_imd B, 10
    ORd ZERO, ZERO, PORA; Zero out PROA
PrintString_Loop:
    LOADb_indirect APA, C ;Get char from string
    BRH_ABS ZERO, PrintString_Exit ;If zero exit
    CMPw C, B ;Is it \n if so make it into /r/n
    BRH_ABS EQUAL, PrintString_NewLine
    JUMP_ABS PrintString_PrintChar
PrintString_NewLine:
    STOREb A, SERIAL_DATA ;Output the /r
PrintString_PrintChar:
    STOREb C, SERIAL_DATA ;Output the character
    ADDd PORA, ONE, PORA
    JUMP_ABS PrintString_Loop
PrintString_Exit:
    POPd PORA
    POPd PRAS
    RTN
    
    
    



BUFFERED_SERIAL_END:
