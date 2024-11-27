#once
#include "cpu_def.asm"
#include "hdd.asm"

;AB is address where to load MBR to
LOAD_MBR:
    PUSHd RA
    ORd AB, ZERO, CD
    LOADd_imd AB, 0
    CALL CopySectorFromDisk
    POPd RA
    RTN

