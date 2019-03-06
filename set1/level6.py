import string
from itertools import combinations

# http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.htm
letter_freq = {
        'e': 21912, 't': 16587, 'a': 14810, 'o': 14003, 'i': 13318,
        'n': 12666, 's': 11450, 'r': 10977, 'h': 10795, 'd': 7874,
        'l': 7253, 'u': 5246, 'c': 4943, 'm': 4761, 'f': 4200, 'y': 3853,
        'w': 3819, 'g': 3693, 'p': 3316, 'b': 2715, 'v': 2019, 'k': 1257,
        'x': 315, 'q': 205, 'j': 188, 'z': 128
        }

def xor(s1, s2):
    return ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))

def score_english(eng_str):
    eng_str = eng_str.lower()
    score = 0
    for c in eng_str:
        if c in letter_freq:
            score += letter_freq[c]
        elif c == " ":
            score += 40000
        elif c in string.printable:
            score += 400
        else:
            score -= 500000
    return score

def single_byte_xor(data, byte):
    xor_str = ""
    for i in data:
        xor_str += chr(ord(i) ^ ord(byte))
    score = score_english(xor_str)
    return score

def brute_byte_xor(data):
    opts = []
    for i in range(256):
        opts.append((single_byte_xor(data, chr(i)), i))
    sol = sorted(opts, reverse=True)
    return chr(sol[0][1])

def hamming_distance(s1, s2):
    s3 = xor(s1, s2)
    ham = 0
    for i in s3:
        ham += bin(ord(i)).count("1")
    return ham

def repeated_key_xor(ctxt, key):
    txt_len = len(ctxt)
    key_len = len(key)
    ptxt = ''
    for i in range(txt_len):
        ptxt += chr(ord(ctxt[i]) ^ ord(key[i % key_len]))
    return ptxt

def calc_normalized_hamming(data, key_size):
    length = len(data)
    chunks = []
    for i in range(4):
        chunks.append(data[i*key_size: (i+1)*(key_size)])
    ham_dists = []
    for i in range(3):
        ham_dists.append(hamming_distance(chunks[i], chunks[i+1]))
    average = float(sum(ham_dists)) / len(ham_dists)
    return (average / key_size)

def break_repeating_key_xor(data):
    sizes = []
    for key_size in range(2, 40):
        normalized_hamming = calc_normalized_hamming(data, key_size)
        sizes.append((normalized_hamming, key_size))
    likely_sizes = sorted(sizes)
    for i in range(5):
        pos_size = likely_sizes[i][1]
        blocks = []
        for i in range(pos_size):
            blocks.append([])
        for j in range(len(data)):
            blocks[j % pos_size] .append(data[j])
        key = ""
        for block in blocks:
            block_str = ''.join(i for i in block)
            key += brute_byte_xor(block_str)
        print repeated_key_xor(data, key)
        raw_input()

def main():
    data = ""
    with open("6.txt", "r") as f:
        data = f.read().strip().decode('base64')
    print data
    raw_input()
    break_repeating_key_xor(data)

if __name__ == '__main__':
    main()
