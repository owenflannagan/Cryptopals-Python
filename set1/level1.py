import base64

def hex_to_b64(data):
    return base64.b64encode(data.decode('hex'))

def main():
    val = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    print hex_to_b64(val)

if __name__ == '__main__':
    main()
