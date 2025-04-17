from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secret import flag, key

cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(bytes(flag, 'utf-8'), AES.block_size))
print(ciphertext.hex())