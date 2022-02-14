import time
from twofish import Twofish
from base64 import b64encode, b64decode

def tfencrypt(infile, outfile, password):
    start_time = time.time()
    infile = 'lolo'*8*4

    bs = 16 #block size 16 bytes or 128 bits
    plaintext = infile
    #plaintext = b64encode(infile.read()).decode('utf-8')
    #print(plaintext)

    if len(plaintext)%bs:
        padded_plaintext=str(plaintext+'%'*(bs-len(plaintext)%bs)).encode('utf-8')
    else:
        padded_plaintext=plaintext.encode('utf-8')
    start_time = time.time()
    for i in range(1000):
        T = Twofish(str.encode(password))
        ciphertext = b''

        for x in range(int(len(padded_plaintext) / bs)):
            ciphertext += T.encrypt(padded_plaintext[x * bs:(x + 1) * bs])
    t = time.time() - start_time
    print("--- %s seconds ---" % (t))
    #outfile.write(ciphertext)


def tfdecrypt(infile, outfile, password):

    bs = 16 #block size 16 bytes or 128 bits
    ciphertext = infile.read()
    T = Twofish(str.encode(password))
    plaintext=b''

    for x in range(int(len(ciphertext)/bs)):
        plaintext += T.decrypt(ciphertext[x*bs:(x+1)*bs])

    outfile.write(str.encode(plaintext.decode('utf-8').strip('%'))) #remove padding


password = '12345'

infile = open('D:/1024.png', 'rb')
outfile = open('D:/fingerprint_kek.BMP', 'wb')
infile = (1024).to_bytes(2, byteorder='big')
tfencrypt(infile, outfile, password)

#with open('D:/fingerprint.BMP', 'rb') as infile, open('D:/fingerprint_kek.BMP', 'wb') as outfile:
#    tfdecrypt(infile, outfile, password)