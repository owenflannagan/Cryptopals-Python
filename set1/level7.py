from Crypto.Cipher import AES

def aes_ecb_decrypt(ctxt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ptxt = cipher.decrypt(ctxt)
    return ptxt

def main():
    with open("7.txt", "r") as f:
        ctxt = f.read().decode("base64")
        key = "YELLOW SUBMARINE"
        print aes_ecb_decrypt(ctxt, key)

if __name__ == '__main__':
    main()
