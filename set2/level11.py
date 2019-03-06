from Crypto.Cipher import AES
import random

def xor(s1, s2):
    return ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))

def pkcs7_pad(data, block_size=16):
    val = block_size - (len(data) % block_size)
    if val == 0:
        val = block_size
    padded_data = data + (chr(val) * val)
    return padded_data

def aes_ecb_decrypt(ctxt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ctxt)

def aes_ecb_encrypt(ptxt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(ptxt)

def aes_cbc_decrypt(ctxt, key, iv='\x00'*16):
    ctxt_blocks = []
    block_size = len(key)
    for i in range(0, len(ctxt), block_size):
        ctxt_blocks.append(ctxt[i:i+block_size])
    ptxt_blocks = []
    block1 = aes_ecb_decrypt(ctxt_blocks[0], key)
    ptxt_blocks.append(block1)
    for i in range(1, len(ctxt_blocks)):
        this_block = aes_ecb_decrypt(ctxt_blocks[i], key)
        ptxt_blocks.append(xor(this_block, ctxt_blocks[i-1]))
    return ''.join(ptxt_blocks)

def aes_cbc_encrypt(ptxt, key, iv='\x00'*16):
    ptxt_blocks = []
    block_size = len(key)
    for i in range(0, len(ptxt), block_size):
        ptxt_blocks.append(ptxt[i:i+block_size])
    ctxt_blocks = []
    pre_1 = xor(ptxt_blocks[0], iv)
    ctxt_blocks.append(aes_ecb_encrypt(pre_1, key))
    for i in range(1, len(ptxt_blocks)):
        pre_block = xor(ptxt_blocks[i], ctxt_blocks[i-1])
        ctxt_blocks.append(aes_ecb_encrypt(pre_block, key))
    return ''.join(ctxt_blocks)

def encryption_oracle(data):
    # Add random bytes before and after string
    before_len = random.randint(5, 10)
    pre_str = ''.join(chr(random.randint(0, 0xff)) for i in range(before_len))
    after_len = random.randint(5, 10)
    post_str = ''.join(chr(random.randint(0, 0xff)) for i in range(after_len))
    data = pre_str + data + post_str
    padded_data = pkcs7_pad(data)
    # Create random key
    key = ''.join(chr(random.randint(0, 0xff)) for i in range(16))
    # Choose ECB or CBC
    opt = random.randint(0, 1)
    if opt == 0:
        print "ECB USED"
        return aes_ecb_encrypt(padded_data, key)
    else:
        print "CBC USED"
        iv = ''.join(chr(random.randint(0, 0xff)) for i in range(16))
        return aes_cbc_encrypt(padded_data, key, iv)

def blackbox_test():
    ptxt = "A"* 48
    ctxt = encryption_oracle(ptxt)
    blocks = []
    for i in range(0, len(ctxt), 16):
        blocks.append(ctxt[i:i+16])
    if len(blocks) != len(set(blocks)):
        print "ECB Mode Detected"
    else:
        print "CBC Mode Detected"
    raw_input()

def main():
    for i in xrange(0x10):
        blackbox_test()

if __name__ == '__main__':
    main()
