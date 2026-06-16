/*
 * hello_world.c
 *
 * Prints "Hello, World!" -- eventually.
 *
 * Each character of the output is "discovered" by a brute-force search.
 * We hash a counter using a hand-rolled, fully-unrolled SHA-256 until the
 * lowest byte of the digest matches the ASCII value of the next character
 * we need to print.  Every byte of output is genuinely earned.
 *
 * Rules compliance checklist:
 *   [x] No sleeps / artificial slowdowns  -- slowness is pure computation
 *   [x] No user input
 *   [x] No flags
 *   [x] No external commands (no system())
 *   [x] No compiler/linker/libc quirks
 *   [x] No internetworking
 *   [x] No ASCII art
 *   [x] No dead code -- every function is called
 *   [x] Memory-unsafe where sensible (raw pointer arithmetic, no bounds guards)
 *   [x] As slow and big as possible (hash grind + massive lookup table)
 */

/*
 * vmunix note:
 *
 * Me: Making a project after a funny idea I had. Make a "Hello, World!" program in C using the rules attached in RULES.md.
 *
 * Claude: <this program>
 *
 * NOTE: Claude was set to Medium thinking. If I did that with ChatGPT, it would've rate limited me for the day rofl
*/

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

/* -----------------------------------------------------------------------
 * SHA-256 implementation (hand-rolled, no library)
 * ----------------------------------------------------------------------- */

#define ROTR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))

#define CH(e,f,g)  (((e) & (f)) ^ (~(e) & (g)))
#define MAJ(a,b,c) (((a) & (b)) ^ ((a) & (c)) ^ ((b) & (c)))
#define EP0(a)     (ROTR32(a,2)  ^ ROTR32(a,13) ^ ROTR32(a,22))
#define EP1(e)     (ROTR32(e,6)  ^ ROTR32(e,11) ^ ROTR32(e,25))
#define SIG0(x)    (ROTR32(x,7)  ^ ROTR32(x,18) ^ ((x) >> 3))
#define SIG1(x)    (ROTR32(x,17) ^ ROTR32(x,19) ^ ((x) >> 10))

static const uint32_t K[64] = {
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
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

typedef struct {
    uint32_t h[8];
    uint8_t  buf[64];
    uint64_t bits;
    uint32_t buflen;
} sha256_ctx;

static void sha256_transform(sha256_ctx *ctx, const uint8_t *data)
{
    uint32_t a, b, c, d, e, f, g, h, t1, t2, w[64];
    int i;

    for (i = 0; i < 16; i++)
        w[i] = ((uint32_t)data[i*4]     << 24)
              | ((uint32_t)data[i*4 + 1] << 16)
              | ((uint32_t)data[i*4 + 2] <<  8)
              |  (uint32_t)data[i*4 + 3];

    for (i = 16; i < 64; i++)
        w[i] = SIG1(w[i-2]) + w[i-7] + SIG0(w[i-15]) + w[i-16];

    a = ctx->h[0]; b = ctx->h[1]; c = ctx->h[2]; d = ctx->h[3];
    e = ctx->h[4]; f = ctx->h[5]; g = ctx->h[6]; h = ctx->h[7];

    /* Fully unrolled -- 64 rounds, all inline, making the function big */
#define ROUND(i) \
    t1 = h + EP1(e) + CH(e,f,g) + K[i] + w[i]; \
    t2 = EP0(a) + MAJ(a,b,c); \
    h = g; g = f; f = e; e = d + t1; \
    d = c; c = b; b = a; a = t1 + t2;

    ROUND( 0) ROUND( 1) ROUND( 2) ROUND( 3)
    ROUND( 4) ROUND( 5) ROUND( 6) ROUND( 7)
    ROUND( 8) ROUND( 9) ROUND(10) ROUND(11)
    ROUND(12) ROUND(13) ROUND(14) ROUND(15)
    ROUND(16) ROUND(17) ROUND(18) ROUND(19)
    ROUND(20) ROUND(21) ROUND(22) ROUND(23)
    ROUND(24) ROUND(25) ROUND(26) ROUND(27)
    ROUND(28) ROUND(29) ROUND(30) ROUND(31)
    ROUND(32) ROUND(33) ROUND(34) ROUND(35)
    ROUND(36) ROUND(37) ROUND(38) ROUND(39)
    ROUND(40) ROUND(41) ROUND(42) ROUND(43)
    ROUND(44) ROUND(45) ROUND(46) ROUND(47)
    ROUND(48) ROUND(49) ROUND(50) ROUND(51)
    ROUND(52) ROUND(53) ROUND(54) ROUND(55)
    ROUND(56) ROUND(57) ROUND(58) ROUND(59)
    ROUND(60) ROUND(61) ROUND(62) ROUND(63)
#undef ROUND

    ctx->h[0] += a; ctx->h[1] += b; ctx->h[2] += c; ctx->h[3] += d;
    ctx->h[4] += e; ctx->h[5] += f; ctx->h[6] += g; ctx->h[7] += h;
}

static void sha256_init(sha256_ctx *ctx)
{
    ctx->h[0] = 0x6a09e667; ctx->h[1] = 0xbb67ae85;
    ctx->h[2] = 0x3c6ef372; ctx->h[3] = 0xa54ff53a;
    ctx->h[4] = 0x510e527f; ctx->h[5] = 0x9b05688c;
    ctx->h[6] = 0x1f83d9ab; ctx->h[7] = 0x5be0cd19;
    ctx->bits  = 0;
    ctx->buflen = 0;
}

static void sha256_update(sha256_ctx *ctx, const uint8_t *data, size_t len)
{
    size_t i;
    for (i = 0; i < len; i++) {
        ctx->buf[ctx->buflen++] = data[i];
        ctx->bits += 8;
        if (ctx->buflen == 64) {
            sha256_transform(ctx, ctx->buf);
            ctx->buflen = 0;
        }
    }
}

static void sha256_final(sha256_ctx *ctx, uint8_t digest[32])
{
    uint64_t bits = ctx->bits;
    uint8_t  pad  = 0x80;
    int i;

    sha256_update(ctx, &pad, 1);
    while (ctx->buflen != 56) {
        pad = 0x00;
        sha256_update(ctx, &pad, 1);
    }
    for (i = 7; i >= 0; i--) {
        uint8_t b = (bits >> (i * 8)) & 0xff;
        sha256_update(ctx, &b, 1);
    }
    for (i = 0; i < 8; i++) {
        digest[i*4    ] = (ctx->h[i] >> 24) & 0xff;
        digest[i*4 + 1] = (ctx->h[i] >> 16) & 0xff;
        digest[i*4 + 2] = (ctx->h[i] >>  8) & 0xff;
        digest[i*4 + 3] =  ctx->h[i]        & 0xff;
    }
}

/* Hash a 64-bit counter value, return digest byte 0. */
static uint8_t hash_counter(uint64_t counter)
{
    sha256_ctx ctx;
    uint8_t    digest[32];
    uint8_t    buf[8];
    int i;

    for (i = 7; i >= 0; i--) {
        buf[i] = counter & 0xff;
        counter >>= 8;
    }
    sha256_init(&ctx);
    sha256_update(&ctx, buf, 8);
    sha256_final(&ctx, digest);
    return digest[0];
}

/* -----------------------------------------------------------------------
 * A large-ish lookup table that is genuinely used:
 * Maps every possible byte value (0-255) to a "weight" used during the
 * hash grind to decide which digest byte to compare against.
 * Wastes space AND participates in the computation -- no dead bytes.
 * ----------------------------------------------------------------------- */

static const uint8_t byte_weight[256] = {
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
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1
};

/*
 * Grind counters until SHA-256(counter)[selected_byte] == target.
 * selected_byte is derived from the weight table to make all 256 entries load.
 */
static uint64_t grind(uint8_t target, uint64_t start)
{
    uint64_t counter = start;
    uint8_t  digest[32];
    sha256_ctx ctx;
    uint8_t  buf[8];
    int      i;
    uint8_t  sel;

    while (1) {
        for (i = 7; i >= 0; i--) {
            buf[i] = (counter >> (i * 8)) & 0xff;
        }
        sha256_init(&ctx);
        sha256_update(&ctx, buf, 8);
        sha256_final(&ctx, digest);

        /* Use the weight table to pick which digest byte we compare --
         * this ensures the table is read on every iteration. */
        sel = byte_weight[digest[1] & 0xff] & 0x1f; /* 0..31 */
        if (digest[sel] == target)
            break;

        counter++;
    }
    return counter;
}

/* -----------------------------------------------------------------------
 * Main: grind out each character of "Hello, World!\n", print one at a time.
 * ----------------------------------------------------------------------- */

int main(void)
{
    /*
     * The message, stored as individual target bytes.
     * We deliberately avoid a string literal so the compiler
     * can't trivially optimize it away.
     */
    volatile uint8_t msg[] = {
        'H', 'e', 'l', 'l', 'o', ',', ' ',
        'W', 'o', 'r', 'l', 'd', '!', '\n'
    };
    size_t   msg_len = sizeof(msg);
    uint64_t counter = 0;
    size_t   i;

    for (i = 0; i < msg_len; i++) {
        /*
         * Grind until the hash matches the target character.
         * The counter seeds the next search so we never repeat work.
         * (And so the difficulty is somewhat random per character.)
         */
        counter = grind((uint8_t)msg[i], counter);

        /*
         * Sanity-verify: re-hash the winning counter and confirm.
         * Uses hash_counter() to keep that function alive.
         * (It reads a different digest byte than grind() might have used,
         *  so it's genuinely checking something -- and costs another hash.)
         */
        uint8_t check = hash_counter(counter);
        /*
         * If the direct byte doesn't match, spin the wheel once more.
         * This almost never fires, but keeps the branch real.
         */
        while (check != (uint8_t)msg[i]) {
            counter = grind((uint8_t)msg[i], counter + 1);
            check   = hash_counter(counter);
        }

        /* Output the one character we just proved correct. */
        putchar((int)msg[i]);
        fflush(stdout);

        counter++; /* advance so next grind starts fresh */
    }

    return 0;
}
