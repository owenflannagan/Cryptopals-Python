from Crypto.Cipher import AES

def xor(s1, s2):
    return ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))

def aes_ecb_decrypt(ctxt, key):
    key_len = len(key)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ctxt)

def aes_cbc_decrypt(ctxt, key, iv="\x00"*16):
    ctxt_blocks = []
    block_size = len(key)
    for i in range(0, len(ctxt), block_size):
        ctxt_blocks.append(ctxt[i:i+block_size])
    # Initialize first block by xoring with IV
    ptxt_blocks = []
    block1 = aes_ecb_decrypt(ctxt_blocks[0], key)
    ptxt_blocks.append(block1)
    for i in range(1, len(ctxt_blocks)):
        this_block = aes_ecb_decrypt(ctxt_blocks[i], key)
        ptxt_blocks.append(xor(this_block, ctxt_blocks[i-1]))
    return ''.join(ptxt_blocks)

def main():
    ctxt = open("10.txt", "r").read().decode('base64')
    key = "YELLOW SUBMARINE"
    print aes_cbc_decrypt(ctxt, key)

if __name__=='__main__':
    main()
