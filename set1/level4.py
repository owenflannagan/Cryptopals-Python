import string
import langdetect

# http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.htm
letter_freq = {
        'e': 21912, 't': 16587, 'a': 14810, 'o': 14003, 'i': 13318,
        'n': 12666, 's': 11450, 'r': 10977, 'h': 10795, 'd': 7874,
        'l': 7253, 'u': 5246, 'c': 4943, 'm': 4761, 'f': 4200, 'y': 3853,
        'w': 3819, 'g': 3693, 'p': 3316, 'b': 2715, 'v': 2019, 'k': 1257,
        'x': 315, 'q': 205, 'j': 188, 'z': 128
        }

def score_english(eng_str):
    eng_str = eng_str.lower()
    score = 0
    for c in eng_str:
        if c in letter_freq:
            score += letter_freq[c]
        elif c == " ":
            score += 80000
        elif c in string.printable:
            score += 400
        else:
            score -= 10000
    return score

def single_byte_xor(data, byte):
    xor_str = ""
    for i in data:
        xor_str += chr(ord(i) ^ ord(byte))
    score = score_english(xor_str)
    return score, xor_str

def main():
    lines = []
    with open("4.txt", "r") as f:
        lines = f.readlines()
    opts = []
    for line in lines:
        line = line.strip().decode('hex')
        for i in range(256):
            opts.append((single_byte_xor(line, chr(i))))
    sol = sorted(opts, reverse=True)
    for i in range(30):
        print sol[i]

if __name__ == '__main__':
    main()
