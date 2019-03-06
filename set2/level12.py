from Crypto.Cipher import AES
import random
import string

secret = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK".decode('base64')
KEY = ''.join(chr(random.randint(0, 0xff)) for i in range(16))

def pkcs7_pad(data, block_size=16)
    val = block_size - (len(data) % block_size)
    if val == 0:
        val = block_size
    padded_data = data + (chr(val) * val)
    return padded_data

def aes_ecb_decrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)

def aes_ecb_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)

def blackbox_encrypt(data):
    data = data + secret
    padded_data = pkcs7_pad(data)
    return aes_ecb_encrypt(padded_data, KEY)

def brute_size():
    i = 0
    prev_size = 99999
    val1 = 0
    while True:
        ctxt = blackbox_encrypt("A"*i)
        size = len(ctxt)
        if size > prev_size:
            val1 = i
            prev_size = size
            i = i+1
            break
        prev_size = size
        i = i+1
    while True:
        ctxt = blackbox_encrypt("A"*i)
        size = len(ctxt)
        if size > prev_size:
            val2 = i
            break
        prev_size = size
        i = i+1
    return (val2 - val1)

def detect_ecb(block_size):
    ptxt = "A"* (block_size * 3)
    ctxt = blackbox_encrypt(ptxt)
    blocks = []
    for i in range(0, len(ctxt), block_size):
        blocks.append(ctxt[i:i+block_size])
    if len(blocks) == len(set(blocks)):
        return 0
    return 1

def aes_ecb_oracle():
    block_size = brute_size()
    print "Block size: " + str(block_size)
    if not detect_ecb(block_size):
        print "Problem!!"
        return
    print "ECB Detected!"
    i = 1
    known = ""
    while i <= 16:
        for j in string.printable:
            ptxt = "A" * (block_size - i) + known + j + "A"* (block_size-i)
            ctxt = blackbox_encrypt(ptxt)
            blocks = []
            for l in range(0, len(ctxt), block_size):
                blocks.append(ctxt[l:l+block_size])
            if blocks[0] == blocks[1]:
                known += j
                i = i+1
                break
    while True:
        found_flag = 0
        for j in string.printable:
            ptxt = known[-(block_size-1):] + j + "A" * (block_size-(i % block_size))
            ctxt = blackbox_encrypt(ptxt)
            blocks = []
            for l in range(0, len(ctxt), block_size):
                blocks.append(ctxt[l:l+block_size])
            if blocks[0] == blocks[(i / block_size) + 1]:
                known += j
                i = i+1
                found_flag = 1
                break
        if found_flag == 0:
            break
    return known

def main():
    print aes_ecb_oracle()

if __name__ == '__main__':
    main()
