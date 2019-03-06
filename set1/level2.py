def xor(x, y):
    return "".join(chr(ord(x1) ^ ord(y1)) for x1, y1 in zip(x, y))

def main():
    v1 = "1c0111001f010100061a024b53535009181c".decode('hex')
    v2 = "686974207468652062756c6c277320657965".decode('hex')
    print xor(v1, v2).encode('hex')

if __name__ == '__main__':
    main()
