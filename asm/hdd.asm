#once
#include "cpu_def.asm"

HDD_LBA0_REGISTER = 0xC0000400
HDD_LBA1_REGISTER = 0xC0000401
HDD_LBA2_REGISTER = 0xC0000402
HDD_LBA3_REGISTER = 0xC0000403
HDD_STATUS_REGISTER = 0xC0000404
HDD_COMMAND_REGISTER = 0xC0000405
HDD_WR_REGISTER = 0xC0000405

HDD_DATA_START = 0xC0000410
HDD_DATA_END = 0xc0000610

HDD_BLOCK_SIZE = 512


; AB is Sector Number, CD is addr to write copy to.
CopySectorFromDisk:
    PUSHd PRAS
    PUSHd PORA
    PUSHd PRBS
    PUSHd PORB
    STOREd AB, HDD_LBA0_REGISTER ;Load Wanted Sector into LBA
    LOADb A, HDD_WR_REGISTER
    LOADd_imd AB, HDD_BLOCK_SIZE
    
    LOADd_imd PRAS, HDD_DATA_START ;Load HDD block start into PRAS
    
    ORd CD, ZERO, PRBS
    
    ORd ZERO, ZERO, PORA
    ORd ZERO, ZERO, PORB
    CopySectorFromDiskLoop:    
    CMPd AB, PORA
    BRH_ABS EQUAL, CopySectorFromDiskExit
    LOADw_indirect APA, C
    STOREw_indirect APB, C
    ADDd ONE, PORA, PORA
    ADDd ONE, PORB, PORB
    JUMP_ABS CopySectorFromDiskLoop
    CopySectorFromDiskExit:
    POPd PRAS
    POPd PORA
    POPd PRBS
    POPd PORB
    RTN
    
; AB is Sector Number, CD is ADDR to copy data from.
CopySectorToDisk:
    PUSHd PRAS
    PUSHd PORA
    PUSHd PRBS
    PUSHd PORB
    STOREd AB, HDD_LBA0_REGISTER ;Load Wanted Sector into LBA
    LOADd_imd AB, HDD_BLOCK_SIZE
    
    LOADd_imd PRAS, HDD_DATA_START ;Load HDD block start into PRAS
    
    ORd CD, ZERO, PRBS
    
    ORd ZERO, ZERO, PORA
    ORd ZERO, ZERO, PORB
    CopySectorFromDiskLoop:    
    CMPd AB, PORA
    BRH_ABS EQUAL, CopySectorFromDiskExit
    LOADw_indirect APB, C
    STOREw_indirect APA, C
    ADDd ONE, PORA, PORA
    ADDd ONE, PORB, PORB
    JUMP_ABS CopySectorFromDiskLoop
    STOREb A, HDD_WR_REGISTER
    CopySectorFromDiskExit:
    POPd PRAS
    POPd PORA
    POPd PRBS
    POPd PORB
    RTN
