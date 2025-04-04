from pwn import *
import hashlib
import time

# Precompute hash_prefixes
hash_map = {}
for i in range(1, 10001):
    h = hashlib.sha256(str(i).encode()).hexdigest()[:6]
    hash_map[h] = i

PORT = 1340

io = remote(HOST, PORT)

# Wait for prompt, send git commit
io.sendlineafter("$", "git commit")
t = str(int(time.time()))  # Estimate commit time
# Capture the commit timestamp
io.recvuntil("Committed.")

# Brute-force the commit hash
log.info(f"Brute-forcing commit ID for timestamp: {commit_time}")

for hash_prefix, rand_val in hash_map.items():
    commit_id = f"{commit_time}-{hash_prefix}"
    io.sendline(f"git snapshot {commit_id}")
    response = io.recvline(timeout=1)

    if b"Success" in response:  # Adjust this check based on expected output
        log.success(f"Found valid commit ID: {commit_id}")
        break

# Keep interactive session open
io.interactive()
