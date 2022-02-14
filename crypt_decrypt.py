import hashlib
import bcrypt
from Crypto.Cipher import AES


def hash_key(ind):
    h = hashlib.blake2b(digest_size=16)
    ind = str.encode(ind)
    h.update(ind)
    key = h.digest()
    hashed = bcrypt.hashpw(key, bcrypt.gensalt())
    return hashed, key


def crypt(pt, key):
    nonce = b'key'
    if type(pt) is int:
        pt = str(pt)
    if type(pt) is not bytes:
        pt = str.encode(pt)
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    ct = cipher.encrypt(pt)
    return ct


def hash_ch(ind, hashed):
    ind = str.encode(ind)
    h = hashlib.blake2b(digest_size=16)
    h.update(ind)
    try:
        bcrypt.checkpw(h.digest(), hashed)
        return bcrypt.checkpw(h.digest(), hashed)
    except ValueError:
        return False


def decrypt(ind, hashed, ct, img=False):
    nonce = b'key'
    ind = str.encode(ind)
    h = hashlib.blake2b(digest_size=16)
    h.update(ind)
    if bcrypt.checkpw(h.digest(), hashed):
        cipher2 = AES.new(h.digest(), AES.MODE_CTR, nonce=nonce)
        pt = cipher2.decrypt(ct)
        if img:
            return pt
        else:
            return pt.decode('utf-8')
    else:
        return None
