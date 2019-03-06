from Crypto.Cipher import A
import random

KEY = ''.join(chr(random.randint(0, 0xff)) for i in range(16))

def pkcs7_pad(data, block_size=16):
    val = block_size - (len(data) % block_size)
    if val == 0:
        val = block_size
    padded_data = data + (chr(val) * val)
    return padded_data

def aes_ecb_encrypt(ptxt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(ptxt)

def aes_ecb_decrypt(ctxt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ctxt)

def cookie_to_obj(cookie):
    params = cookie.split("&")
    jso = dict(param.split("=") for param in params)

def sanitize(data):
    return data.replace("&", "").replace("=", "")

def profile_for(email):
    email = sanitize(email)
    cookie = "email=" + email + "&uid=10&role=user"
    my_jso = cookie_to_obj(cookie)
    return cookie

def blackbox_cookie(data):
    cookie = profile_for(data)
    padded_cookie = pkcs7_pad(cookie)
    ctxt = aes_ecb_encrypt(padded_cookie, KEY)
    return ctxt

def make_block(data):
    block = pkcs7_pad(data)
    block_size = len(block)
    for i in range(block_size):
        ptxt = "A"*i + block + block
        ctxt = blackbox_cookie(ptxt)
        blocks = []
        for i in range(0, len(ctxt), block_size):
            blocks.append(ctxt[i:i+block_size])
        if len(blocks) != len(set(blocks)):
            for i in range(len(blocks)-1):
                if blocks[i] == blocks[i+1]:
                    return blocks[i]

def find_and_replace(block_f, block_r):
    block_size = len(block_f)
    for i in range(block_size):
        ptxt = "A"*i
        ctxt = blackbox_cookie(ptxt)
        blocks = []
        for i in range(0, len(ctxt), block_size):
            blocks.append(ctxt[i:i+block_size])
        if block_f in blocks:
            blocks = [block_r if block==block_f else block for block in blocks]
            return ''.join(blocks)

def get_admin_profile():
    admin_block = make_block("admin")
    user_block = make_block("user")
    print admin_block
    raw_input()
    print user_block
    raw_input()
    cookie = find_and_replace(user_block, admin_block)
    print cookie
    print aes_ecb_decrypt(cookie, KEY)

def main():
    cookie_to_obj("foo=bar&baz=qux&zap=zazzle")
    get_admin_profile()
    return

if __name__ == '__main__':
    main()
