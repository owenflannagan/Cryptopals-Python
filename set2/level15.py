def validate_padding(data):
    length = len(data)
    pad = data[length-1]
    for i in range(ord(pad)):
        if data[length-1-i] != pad:
            raise Exception("Invalid padding")
    return data[:-ord(pad)]

def main():
    print validate_padding("ICE ICE BABY\x04\x04\x04\x04")
    print validate_padding("ICE ICE BABY\x05\x05\x05\x05")

if __name__ == '__main__':
    main()
