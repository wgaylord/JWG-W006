#once
#include "cpu_def.asm"

INIT:

LOADd_imd SP, 0x53ff

LOADd_imd PRAS, 0x400
LOADd_imd PORA, 0
LOADw_imd B, 0xaa

LOADd_imd AB, INIT_MEM_COUNT
CALL_ABS SerialPrintString
INIT_LOOP:
LOADw_imd C, 13
STOREb C, 0xC0000000
CALL_ABS INIT_WRITE_NUM
LOADb_indirect APA, D
STOREb_indirect APA, B
LOADb_indirect APA, A
STOREb_indirect APA, D
STOREb_indirect APA, ZERO
ADDd PORA, ONE, PORA
CMPw A, B
BRH_ABS EQUAL, INIT_LOOP

ADDd PRAS, PORA, AB

JUMP_ABS MAIN


INIT_WRITE_NUM:
    PUSHd RA
    PUSHd AB
    LOADd_imd PRBS, 0x400
    LOADd_imd PORB, 32
    STOREb_indirect APB, ZERO
    SUBd PORB, ONE, PORB
    ORd APA, ZERO, IJ
    LOADd_imd CD, 10
    LOADd_imd GH, 0x30
    INIT_WRITE_NUM_LOOP:
    REMd IJ, CD, EF
    DIVd IJ, CD, IJ
    ADDd EF, GH, EF
    STOREb_indirect APB, E
    SUBd PORB, ONE, PORB
    CMPd IJ, ZERO
    BRH_ABS EQUAL, INIT_WRITE_NUM_EXIT
    JUMP_ABS INIT_WRITE_NUM_LOOP
    INIT_WRITE_NUM_EXIT:
    ADDd APB, ONE, AB
    CALL_ABS SerialPrintString
    POPd AB
    POPd RA
    RTN
    
INIT_MEM_COUNT:
#d "Counting and testing memory.\n\0"

#include "buffered_serial.asm"
