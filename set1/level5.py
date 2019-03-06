def repeated_key_xor(ptxt, key):
    txt_len = len(ptxt)
    key_len = len(key)
    ctxt = ''
    for i in range(txt_len):
        ctxt += chr(ord(ptxt[i]) ^ ord(key[i % key_len]))
    return ctxt

def main():
    ptxt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = "ICE"
    print repeated_key_xor(ptxt, key).encode('hex')

if __name__ == '__main__':
    main()
