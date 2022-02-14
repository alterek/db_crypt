import time
import bcrypt
import struct
from twofish import Twofish
from Crypto.Cipher import AES, DES, DES3, Blowfish
from Crypto.Hash import BLAKE2b
from Crypto.Random import get_random_bytes
from struct import pack
from base64 import b64encode, b64decode

def bin_to_float(b):
    return struct.unpack('<d', struct.pack('<Q', int(b, 2)))[0]
def float_to_bin(f):
    return '{:b}'.format(struct.unpack('<Q', struct.pack('<d', f))[0])

def AES_crypt(data):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CTR)

    ciphertext = cipher.encrypt(data)
    # nonce = cipher.nonce
    # cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, use_aesni=True)
    # pt = cipher.decrypt(ciphertext)
    # print("The message was: ", pt)

def DES_crypt(data):
    key = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_OFB)

    msg = cipher.iv + cipher.encrypt(data)

def Triple_DES_crypt(data):
    key = get_random_bytes(24)
    cipher = DES3.new(key, DES3.MODE_CFB)

    msg = cipher.iv + cipher.encrypt(data)

def Blowfish_crypt(data):
    key = get_random_bytes(16)
    bs = Blowfish.block_size
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)

    plen = bs - len(data) % bs
    padding = [plen] * plen
    padding = pack('b' * plen, *padding)
    msg = cipher.iv + cipher.encrypt(data + padding)


#image = open('D:/fingerprint.BMP', 'rb')
n = 1000
my_str = 'D:/4096.jpg'
image = open(my_str, 'rb')
card = image.read()
#card = b'5555444433332222'



start_time = time.time()
for i in range(n):
    image = open(my_str, 'rb')
    card = image.read()
    AES_crypt(card)
print("AES sec: ", time.time() - start_time)

start_time = time.time()
for i in range(n):
    image = open(my_str, 'rb')
    card = image.read()
    DES_crypt(card)
print("DES sec: ", time.time() - start_time)

start_time = time.time()
for i in range(10):
    image = open(my_str, 'rb')
    card = image.read()
    Triple_DES_crypt(card)
print("3DES sec: ", (time.time() - start_time)*100)

start_time = time.time()
for i in range(n):
    image = open(my_str, 'rb')
    card = image.read()
    Blowfish_crypt(card)
print("Blowfish sec: ", time.time() - start_time)



password = b"super secret password"
#password = b"super secret password super secret password super secret password super secret password"
salt = b'$2b$12$Jmc4jjbpHUCHt2RkH.V5le'
hashed = bcrypt.hashpw(password, salt)
# print(len(hashed))
bcrypt.checkpw(password, hashed)

h_obj = BLAKE2b.new(digest_bits=64)
h_obj.update(b'Some data')
# print(h_obj.digest())

