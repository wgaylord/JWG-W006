#include "cpu_def.asm"
#include "init.asm"
#include "buffered_serial.asm"

MAIN:

LOADd_imd CD, STRING0

CALL_ABS SerialPrintString

CALL_ABS SerialWriteDWord

LOADd_imd AB, STRING3

CALL_ABS SerialPrintString

MAIN_LOOP:

LOADd_imd AB, STRING1

CALL_ABS SerialPrintString

LOADd_imd AB, STRING2

CALL_ABS SerialPrintString

CALL_ABS SerialGetChar

JUMP_ABS MAIN_LOOP

HALT
#d 0x00000000

STRING0:
#d "Started with \0"

STRING3:
#d " Bytes of RAM avaliable.\n\0"

STRING1:
#d "This is a test!\nDoes \\n work? \n YES!\n\0"
STRING2:
#d "Hit any key to run again!\n"

