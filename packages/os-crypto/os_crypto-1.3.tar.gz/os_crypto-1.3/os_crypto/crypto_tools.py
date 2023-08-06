########################################################
# this module meant to provide crypto handling actions #
########################################################

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# will encrypt a data block
def encrypt(data, key, iv, mode=AES.MODE_CBC, padding_size=AES.block_size):
    encryption_cipher = AES.new(key, mode, iv)
    return encryption_cipher.encrypt(pad(data, padding_size))


# will decrypt a data block
def decrypt(data, key, iv, mode=AES.MODE_CBC, padding_size=AES.block_size):
    cipher = AES.new(key, mode, iv)
    return cipher.decrypt(pad(data, padding_size))
