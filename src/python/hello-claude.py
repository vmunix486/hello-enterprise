#!/usr/bin/env python3
#
# hello_world.py
#
# Prints "Hello, World!" -- eventually.
#
# Each character of the output is "discovered" by brute-force SHA-256 grinding.
# We hash a counter until a digest byte matches the ASCII value of the next
# character we need to print. Every byte of output is genuinely earned.
#
# Rules compliance checklist:
#   [x] No sleeps / artificial slowdowns  -- slowness is pure computation
#   [x] No user input
#   [x] No flags
#   [x] No external commands (no os.system(), subprocess, etc.)
#   [x] No internetworking
#   [x] No ASCII art
#   [x] No dead code -- every function and data structure is used
#   [x] As slow and big as possible (hand-rolled SHA-256 + massive tables)

import sys
import struct

# vmunix note:
#
# This was on the same chat as the C version.
#
# Message:
# Can you now do it for python?
#
# Reply:
# <this program>
#
# This is the slowest one by far rofl

# ---------------------------------------------------------------------------
# Hand-rolled SHA-256 -- no hashlib allowed (that would be too easy and fast)
# ---------------------------------------------------------------------------

MASK32 = 0xFFFFFFFF

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

H0 = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
]

def rotr32(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK32

def sha256_transform(h, chunk):
    w = list(struct.unpack('>16I', chunk))
    for i in range(16, 64):
        s0 = rotr32(w[i-15], 7) ^ rotr32(w[i-15], 18) ^ (w[i-15] >> 3)
        s1 = rotr32(w[i-2], 17) ^ rotr32(w[i-2],  19) ^ (w[i-2]  >> 10)
        w.append((w[i-16] + s0 + w[i-7] + s1) & MASK32)

    a, b, c, d, e, f, g, hh = h

    # All 64 rounds written out explicitly -- makes this function very large
    # and ensures the interpreter has maximum work to do per call.
    def rnd(a, b, c, d, e, f, g, hh, k, wi):
        S1   = rotr32(e, 6) ^ rotr32(e, 11) ^ rotr32(e, 25)
        ch   = (e & f) ^ (~e & g)
        temp1 = (hh + S1 + ch + k + wi) & MASK32
        S0   = rotr32(a, 2) ^ rotr32(a, 13) ^ rotr32(a, 22)
        maj  = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (S0 + maj) & MASK32
        return (temp1 + temp2) & MASK32, a, b, c, (d + temp1) & MASK32, e, f, g

    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 0], w[ 0])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 1], w[ 1])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 2], w[ 2])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 3], w[ 3])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 4], w[ 4])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 5], w[ 5])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 6], w[ 6])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 7], w[ 7])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 8], w[ 8])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[ 9], w[ 9])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[10], w[10])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[11], w[11])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[12], w[12])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[13], w[13])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[14], w[14])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[15], w[15])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[16], w[16])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[17], w[17])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[18], w[18])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[19], w[19])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[20], w[20])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[21], w[21])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[22], w[22])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[23], w[23])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[24], w[24])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[25], w[25])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[26], w[26])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[27], w[27])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[28], w[28])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[29], w[29])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[30], w[30])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[31], w[31])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[32], w[32])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[33], w[33])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[34], w[34])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[35], w[35])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[36], w[36])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[37], w[37])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[38], w[38])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[39], w[39])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[40], w[40])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[41], w[41])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[42], w[42])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[43], w[43])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[44], w[44])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[45], w[45])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[46], w[46])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[47], w[47])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[48], w[48])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[49], w[49])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[50], w[50])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[51], w[51])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[52], w[52])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[53], w[53])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[54], w[54])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[55], w[55])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[56], w[56])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[57], w[57])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[58], w[58])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[59], w[59])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[60], w[60])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[61], w[61])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[62], w[62])
    a,b,c,d,e,f,g,hh = rnd(a,b,c,d,e,f,g,hh, K[63], w[63])

    return [
        (h[0] + a)  & MASK32,
        (h[1] + b)  & MASK32,
        (h[2] + c)  & MASK32,
        (h[3] + d)  & MASK32,
        (h[4] + e)  & MASK32,
        (h[5] + f)  & MASK32,
        (h[6] + g)  & MASK32,
        (h[7] + hh) & MASK32,
    ]

def sha256_digest(data: bytes) -> bytes:
    """Full SHA-256 with padding, hand-rolled."""
    msg = bytearray(data)
    bit_len = len(data) * 8
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0x00)
    msg += struct.pack('>Q', bit_len)

    h = list(H0)
    for i in range(0, len(msg), 64):
        h = sha256_transform(h, bytes(msg[i:i+64]))

    return struct.pack('>8I', *h)

# ---------------------------------------------------------------------------
# A large lookup table used to select which digest byte to test.
# Every entry is consulted during the grind loop -- no dead data.
# ---------------------------------------------------------------------------

BYTE_WEIGHT = [
     7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97,101,103,107,109,113,127,131,137,139,149,
   151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,
   239,241,251,  2,  4,  6,  8, 10, 12, 14, 16, 18, 20, 22, 24, 26,
    28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58,
    60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90,
    92, 94, 96, 98,100,102,104,106,108,110,112,114,116,118,120,122,
   124,126,128,130,132,134,136,138,140,142,144,146,148,150,152,154,
   156,158,160,162,164,166,168,170,172,174,176,178,180,182,184,186,
   188,190,192,194,196,198,200,202,204,206,208,210,212,214,216,218,
   220,222,224,226,228,230,232,234,236,238,240,242,244,246,248,250,
   252,254,  1,  3,  5,  9, 15, 21, 25, 27, 33, 35, 39, 45, 51, 55,
    63, 69, 75, 77, 87, 91, 93, 99,111,115,117,123,125,129,135,141,
   143,153,155,159,165,171,175,177,183,189,195,201,203,213,215,219,
   221,225,231,235,237,243,245,249,253,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,
]

# ---------------------------------------------------------------------------
# Grind: hash counters until a digest byte matches the target character.
# ---------------------------------------------------------------------------

def grind(target: int, start: int) -> int:
    counter = start
    while True:
        digest = sha256_digest(struct.pack('>Q', counter))
        # Use BYTE_WEIGHT to select which digest byte to test --
        # this ensures every table entry can be reached.
        sel = BYTE_WEIGHT[digest[1]] & 0x1f   # 0..31, always in digest range
        if digest[sel] == target:
            return counter
        counter += 1

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Store the target message as a list of ints so Python can't short-circuit
    # and just print a string literal.
    msg = [72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33, 10]
    #       H    e    l    l    o   ,       W    o    r    l    d    !   \n

    counter = 0
    for target in msg:
        counter = grind(target, counter)

        # Verification pass using a fresh hash to confirm the result.
        check_digest = sha256_digest(struct.pack('>Q', counter))
        while check_digest[0] != target:
            counter = grind(target, counter + 1)
            check_digest = sha256_digest(struct.pack('>Q', counter))

        sys.stdout.write(chr(target))
        sys.stdout.flush()
        counter += 1

if __name__ == '__main__':
    main()
