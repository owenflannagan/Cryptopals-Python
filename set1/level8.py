def detect_ecb_encryption(data):
    chunks = []
    for i in range(0, len(data), 16):
        chunks.append(data[i: i+16])
    if (len(chunks) != len(set(chunks))):
        print "ECB Mode Detected!"
    return

def main():
    lines = []
    with open("8.txt", "r") as f:
        lines = f.readlines()
    opts = []
    for line in lines:
        line = line.strip().decode('hex')
        detect_ecb_encryption(line)

if __name__=='__main__':
    main()
