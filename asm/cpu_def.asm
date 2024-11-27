#once
#subruledef register16
{
   ZERO => 0
   ONE  => 1
   
   A => 2
   B => 3
   C => 4
   D => 5
   E  => 6
   F  => 7
   G  => 8
   H  => 9
   I  => 10
   J  => 11
   K  => 12
   L  => 13
   M  => 14
   N  => 15
   
}

#subruledef register32
{
    ZERO => 0
    ONE => 1

   AB => 2
   CD => 4
   EF => 6
   GH => 8
   IJ => 10
   KL => 12
   MN => 14
   
   PRAS => 16
   PRBS => 17
   
   PORA =>18
   PORB => 19
   
   APA => 20
   APB => 21
   
   SP => 22
   
   RA => 23
   
   IR => 24
}

#subruledef condition
{
	
	CARRY => 1
	ZERO => 2
	GREATER => 4
	EQUAL => 8
	
}

#ruledef
{

    NOP  => 0x00 @ 0x00 @ 0x00 @ 0x00 ;NOP
	ADDw {a: register16}, {b: register16}, {c: register16} => 0x01 @ a`8 @ b`8 @ c`8
	ADDd {a: register32}, {b: register32}, {c: register32} => 0x02 @ a`8 @ b`8 @ c`8
	SUBw {a: register16}, {b: register16}, {c: register16} => 0x03 @ a`8 @ b`8 @ c`8
	SUBd {a: register32}, {b: register32}, {c: register32} => 0x04 @ a`8 @ b`8 @ c`8
	MULTw {a: register16}, {b: register16}, {c: register16} => 0x05 @ a`8 @ b`8 @ c`8
	MULTd {a: register32}, {b: register32}, {c: register32} => 0x06 @ a`8 @ b`8 @ c`8
	DIVw {a: register16}, {b: register16}, {c: register16} => 0x07 @ a`8 @ b`8 @ c`8
	DIVd {a: register32}, {b: register32}, {c: register32} => 0x08 @ a`8 @ b`8 @ c`8
	REMw {a: register16}, {b: register16}, {c: register16} => 0x09 @ a`8 @ b`8 @ c`8
	REMd {a: register32}, {b: register32}, {c: register32} => 0x0A @ a`8 @ b`8 @ c`8
	ORw {a: register16}, {b: register16}, {c: register16} => 0x0B @ a`8 @ b`8 @ c`8
	ORd {a: register32}, {b: register32}, {c: register32} => 0x0C @ a`8 @ b`8 @ c`8
	ANDw {a: register16}, {b: register16}, {c: register16} => 0x0D @ a`8 @ b`8 @ c`8
	ANDd {a: register32}, {b: register32}, {c: register32} => 0x0E @ a`8 @ b`8 @ c`8
	XORw {a: register16}, {b: register16}, {c: register16} => 0x1F @ a`8 @ b`8 @ c`8
	XORd {a: register32}, {b: register32}, {c: register32} => 0x10 @ a`8 @ b`8 @ c`8
	
	SHIFTLw {a: register16}, {c: register16} => 0x11 @ a`8 @ 0x00 @ c`8
	SHIFTLd {a: register32}, {c: register32} => 0x12 @ a`8 @ 0x00 @ c`8
	SHIFTRw {a: register16}, {c: register16} => 0x13 @ a`8 @ 0x00 @ c`8
	SHIFTRd {a: register32}, {c: register32} => 0x14 @ a`8 @ 0x00 @ c`8
	
	NOTw {a: register16}, {c: register16} => 0x15 @ a`8 @ 0x00 @ c`8
	NOTd {a: register32}, {c: register32} => 0x16 @ a`8 @ 0x00 @ c`8
	
	CMPw {a: register16}, {b: register16} => 0x17 @ a`8 @ b`8 @ 0x00
	CMPd {a: register32}, {b: register32} => 0x18 @ a`8 @ b`8 @ 0x00

	PUSHb {a: register16} => 0x19 @ a`8 @ 0x00 @ 0x00
	PUSHw {a: register16} => 0x1A @ a`8 @ 0x00 @ 0x00
	PUSHd {a: register32} => 0x1B @ a`8 @ 0x00 @ 0x00
	
	POPb {c: register16} => 0x1C @ 0x00 @ 0x00 @ c`8
	POPw {c: register16} => 0x1D @ 0x00 @ 0x00 @ c`8
	POPd {c: register32} => 0x1E @ 0x00 @ 0x00 @ c`8
	
	BRH_ABS {cond: condition}, {addr: u32} => 0x1F @ cond`8 @ 0x00 @ 0x00 @ le(addr`32)
	BRH_REG {cond: condition}, {reg: register32} => 0x20 @ cond`8 @ reg`8 @ 0x00
	
	JUMP_ABS {addr: u32} => 0x21 @ 0x00 @ 0x00 @ 0x00 @ le(addr`32)
	JUMP_REG {reg: register32} => 0x22 @ 0x00 @ reg`8 @ 0x00
	
	CALL_ABS {addr: u32} => 0x23 @ 0x00 @ 0x00 @ 0x00 @ le(addr`32)
	CALL_REG {reg: register32} => 0x24 @ 0x00 @ reg`8 @ 0x00
	
	LOADw_imd {reg: register16}, {value: u16} => 0x25 @ 0x00 @ 0x00 @ reg`8 @ le(value`16) @ 0x00 @ 0x00
	LOADd_imd {reg: register32}, {value: u32} => 0x26 @ 0x00 @ 0x00 @ reg`8 @ le(value`32)
	
	LOADb {reg: register16}, {addr: u32} => 0x27 @ 0x00 @ 0x00 @ reg`8 @ le(addr`32)
	LOADw {reg: register16}, {addr: u32} => 0x28 @ 0x00 @ 0x00 @ reg`8 @ le(addr`32)
	LOADd {reg: register32}, {addr: u32} => 0x29 @ 0x00 @ 0x00 @ reg`8 @ le(addr`32)
	
	LOADb_indirect {b: register32}, {c: register16} => 0x2A @ 0x00 @ b`8 @ c`8
	LOADw_indirect {b: register32}, {c: register16} => 0x2B @ 0x00 @ b`8 @ c`8
	LOADd_indirect {b: register32}, {c: register32} => 0x2C @ 0x00 @ b`8 @ c`8
	
	LOAD_flag {c: register16} => 0x2D @ 0x00 @ 0x00 @ c`8
	LOAD_status {c: register16} => 0x2E @ 0x00 @ 0x00 @ c`8
	
	STOREb {reg: register16}, {addr: u32} => 0x2F @ reg`8 @ 0x00 @ 0x00 @ le(addr`32)
	STOREw {reg: register16}, {addr: u32} => 0x30 @ reg`8 @ 0x00 @ 0x00 @ le(addr`32)
	STOREd {reg: register32}, {addr: u32} => 0x31 @ reg`8 @ 0x00 @ 0x00 @ le(addr`32)
	
	STOREb_indirect {a: register32}, {b: register16} => 0x32 @ a`8 @ b`8 @ 0x00
	STOREw_indirect {a: register32}, {b: register16} => 0x33 @ a`8 @ b`8 @ 0x00
	STOREd_indirect {a: register32}, {b: register32} => 0x34 @ a`8 @ b`8 @ 0x00
	
	STORE_flag {a: register16} => 0x35 @ a`8 @ 0x00 @ 0x00
	
	INTERRUPT_ABS {a: register16} => 0x36 @ a`8 @ 0x00 @ 0x00
	
	INTERRUPT_REG {a: register16} => 0x37 @ a`8 @ 0x00 @ 0x00
	
	LOAD_STOREb {load: register16}, {store: register16}, {addr: u32} => 0x38 @ load`8 @ 0x00 @ store`8 @ le(addr`32)
	LOAD_STOREw {load: register16}, {store: register16}, {addr: u32} => 0x39 @ load`8 @ 0x00 @ store`8 @ le(addr`32)
	
	LOAD_STOREb_indirect {load: register16}, {store: register16}, {addr: register32} => 0x40 @ load`8 @ addr`8 @ store`8
	LOAD_STOREw_indirect {load: register16}, {store: register16}, {addr: register32} => 0x41 @ load`8 @ addr`8 @ store`8

	
	
	P_NOP => 0x80 @ 0x00 @ 0x00 @ 0x00
	
	STORE_status {a: register16} => 0x81 @ a`8 @ 0x00 @ 0x00
	
	LOAD_PTI {c: register32} => 0x82 @ 0x00 @ 0x00 @ c`8
	STORE_PTI {a: register32} => 0x83 @ a`8 @ 0x00 @ 0x00
	
	LOAD_IVT {c: register32} => 0x84 @ 0x00 @ 0x00 @ c`8
	STORE_IVT {a: register32} => 0x85 @ a`8 @ 0x00 @ 0x00
	
	RETURN_INT => 0x86 @ 0x00 @ 0x00 @ 0x00
	DISABLE_INT => 0x87 @ 0x00 @ 0x00 @ 0x00
	ENABLE_INT => 0x88 @ 0x00 @ 0x00 @ 0x00
	
	HALT => 0xff @ 0x00 @ 0x00 @ 0x00
	
	addr {add} => le(add`32)
	
	RTN => asm { JUMP_REG RA }
	
}

