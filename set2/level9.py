def pkcs7_pad(data, block_size=16):
    val = block_size - (len(data) % block_size)
    if val == 0:
        val = block_size
    padded_data = data + (chr(val) * val)
    return padded_data

def main():
    print pkcs7_pad("YELLOW SUBMARINE", 20)

if __name__ == '__main__':
    main()
