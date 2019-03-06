from Crypto.Cipher import AES
import random

KEY = ''.join(chr(random.randint(0, 0xff)) for i in range(16))
IV = ''.join(chr(random.randint(0, 0xff)) for i in range(16))

def xor(s1, s2):
    return ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))

def pkcs7_pad(data, block_size=16):
    val = block_size - (len(data) % block_size)
    if val == 0:
        val = block_size
    padded_data = data + (chr(val) * val)
    return padded_data

def aes_cbc_decrypt(ctxt, key, iv="\x00"*16):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(ctxt)

def aes_cbc_encrypt(ptxt, key, iv="\x00"*16):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(ptxt)

def prep_cookie(data):
    data = data.replace("=", "\"=\"").replace(";", "\";\"")
    cookie = "comment1=cooking%20MCs;userdata=" + data + ";comment2=%20like%20a%20pound%20of%20bacon"
    return cookie

def is_admin(cookie):
    ptxt = aes_cbc_decrypt(cookie, KEY, IV)
    if ";admin=true;" in ptxt:
        print "You are an admin"
    else:
        print "Failure"

def encrypt_cookie(data):
    cookie = prep_cookie(data)
    padded_cookie = pkcs7_pad(cookie)
    return aes_cbc_encrypt(padded_cookie, KEY, IV)

def forge_admin():
    next_block = ";comment2=%20like%20a%20pound%20of%20bacon"[:16]
    want_block = ";admin=true;com="
    xor_mask = xor(next_block, want_block)
    ctxt = encrypt_cookie("A"*16)
    ctxt2 = encrypt_cookie("B"*16)
    for i in range(0, len(ctxt), 16):
        if (ctxt[i:i+16] != ctxt2[i:i+16]):
            break
    cur_block = ctxt[i:i+16]
    new_block = xor(cur_block, xor_mask)
    new_ctxt = ctxt.replace(cur_block, new_block)
    print aes_cbc_decrypt(new_ctxt, KEY, IV)
    is_admin(new_ctxt)

def main():
    forge_admin()
    return

if __name__=='__main__':
    main()
