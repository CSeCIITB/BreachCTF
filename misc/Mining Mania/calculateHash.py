import hashlib
import struct

def little_endian(hex_str, length):
    """Convert a hex string to little-endian format with a fixed length."""
    return bytes.fromhex(hex_str)[::-1].hex().ljust(length * 2, '0')

def calculate_block_hash(block_data):
    """Calculate the block hash from block data."""
    version = struct.pack('<I', block_data['version']).hex()  # 4 bytes, little-endian
    prev_block = little_endian(block_data['previousblockhash'], 32)  # 32 bytes, little-endian
    merkle_root = little_endian(block_data['merkleroot'], 32)  # 32 bytes, little-endian
    timestamp = struct.pack('<I', block_data['time']).hex()  # 4 bytes, little-endian
    bits = little_endian(block_data['bits'], 4)  # 4 bytes, little-endian
    nonce = struct.pack('<I', block_data['nonce']).hex()  # 4 bytes, little-endian
    
    # Concatenate block header fields
    block_header_hex = version + prev_block + merkle_root + timestamp + bits + nonce
    block_header_bin = bytes.fromhex(block_header_hex)
    
    # Perform double SHA-256
    hash1 = hashlib.sha256(block_header_bin).digest()
    hash2 = hashlib.sha256(hash1).digest()
    
    # Convert final hash to little-endian
    block_hash = hash2[::-1].hex()
    return block_hash

# Example block data (from your block)
block_data = {
    "version": 1,
    "previousblockhash": "00000000b5c44c71fc6d438a944f5b57c8fdb719dd7639fa94a14576a374598a",
    "merkleroot": "313f10ccf958e0035d451d48cb14fe2c3bd4bbc4df4b862793ff020d1d59816f",
    "time": 1236693063,
    "bits": "1d00ffff",
    "nonce": 3355541045
}

# Compute and print the recalculated block hash
recomputed_hash = calculate_block_hash(block_data)
print("Recomputed Block Hash:", recomputed_hash)
