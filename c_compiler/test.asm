JUMP_ABS __init__
;['funcDef', 'main', []]
main:
PUSHd RA
PUSHd PRAS
PUSHd PORA
ORd SP, ZERO, PRAS
ORd ZERO, ZERO, PORA
;['loadVarAsArg', 'TestString']
PUSHd AB
LOADd EF, TestString
ORd ZERO, EF, AB
;['callFunc', 'printString']
; Byte Arg Count 2
CALL_ABS printString
POPd AB
;['return']
POPd PORA
POPd PRAS
POPd RA 
JUMP_REG RA
;['funcDef', 'printString', [{'name': 'str', 'type': 'pointer_char'}]]
printString:
PUSHd RA
PUSHd PRAS
PUSHd PORA
ORd SP, ZERO, PRAS
ORd ZERO, ZERO, PORA
PUSHw ZERO
;['arrayAccess', 'index', 'str']
;['binOpLeft']
;['loadConst', 0]
;['binOpRight']
;['binOp', '!=']
;['while', 'printString']
;['arrayAccess', 'index', 'str']
;['assign']
;['binOpLeft']
;['loadConst', 1]
;['binOpRight']
;['binOp', '+']
;['binOpLeft']
;['loadConst', 3]
;['binOpRight']
;['binOp', '+']
;['assign']
;['while_end', 'printString']
;['return']
POPd PORA
POPd PRAS
POPd RA 
JUMP_REG RA
__init__:
LOADd_imd AB, 3221225472
STOREd AB, serial
LOADw_imd A, 2
STOREb A, serial2
LOADd_imd AB, 0
LOADd_imd SP, stack
JUMP_ABS main
#addr 0x4fff
serial:
#d 00`32
serial2:
#d 00`8
TestString:
#d 00`32
stack:
