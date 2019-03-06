import string

# http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
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
            score += 10000
        elif ord(c) >= 0x20 and ord(c) < 0x79:
            score += 100
        else:
            score -= 5000
    return score


def single_byte_xor(data, byte):
    xor_str = ""
    for i in data:
        xor_str += chr(ord(i) ^ ord(byte))
    score = score_english(xor_str)
    return score, xor_str

def main():
    val = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736".decode('hex')
    opts = []
    for i in range(256):
        opts.append((single_byte_xor(val, chr(i))))
    sol = sorted(opts, reverse=True)
    for i in range(3):
        print sol[i]

if __name__ == '__main__':
    main()
