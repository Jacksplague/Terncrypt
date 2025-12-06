#!/usr/bin/env python3
"""
Balanced-ternary block cipher (toy / educational).

Core block cipher:
- Block size: 108 balanced trits  (T,0,1)
- Key size:   162 balanced trits
- Rounds:     10
- Field:      GF(3^3) with modulus x^3 + 2x + 1
- Structure:  AES-like (SubTrytes, ShiftRows, MixColumns, AddRoundKey)

Helpers:
- bytes <-> balanced trits (6 trits per byte) for *plaintext and recovered data*
- CTR mode over trits for arbitrary-length streams
- Packed representation of ternary ciphertext/tag as bytes
- AEAD-style authenticated encryption:
    encrypt_aead_bytes(...)
    decrypt_aead_bytes(...)

IMPORTANT:
- Ciphertext and tag bytes are packed ternary and are NOT compatible with
  trits_to_bytes / bytes_to_trits (those are only for plaintext and internal use).
"""

# ----------------------------
# Balanced trit utilities
# ----------------------------

TRIT_TO_RES = {'T': 2, '0': 0, '1': 1}   # -1 -> residue 2 mod 3
RES_TO_TRIT = {0: '0', 1: '1', 2: 'T'}

def trit_str_to_residues(trits: str) -> list[int]:
    return [TRIT_TO_RES[c] for c in trits]

def residues_to_trit_str(res: list[int]) -> str:
    return ''.join(RES_TO_TRIT[r % 3] for r in res)

def trit_add_char(a: str, b: str) -> str:
    """Balanced ternary 'XOR': addition mod 3 on residues."""
    return RES_TO_TRIT[(TRIT_TO_RES[a] + TRIT_TO_RES[b]) % 3]

def trit_add_block(a: str, b: str) -> str:
    """Add two equal-length trit strings mod 3 (balanced)."""
    return ''.join(trit_add_char(x, y) for x, y in zip(a, b))

def trit_sub_char(a: str, b: str) -> str:
    """Balanced ternary subtraction: (a - b) mod 3 on residues."""
    return RES_TO_TRIT[(TRIT_TO_RES[a] - TRIT_TO_RES[b]) % 3]

def trit_sub_block(a: str, b: str) -> str:
    """Subtract two equal-length trit strings: a - b (mod 3)."""
    return ''.join(trit_sub_char(x, y) for x, y in zip(a, b))

# ----------------------------
# Tryte <-> GF(3^3) encoding
# ----------------------------

def tryte_from_trits(t2: str, t1: str, t0: str) -> int:
    r2 = TRIT_TO_RES[t2]
    r1 = TRIT_TO_RES[t1]
    r0 = TRIT_TO_RES[t0]
    return 9 * r2 + 3 * r1 + r0  # 0..26

def trits_from_tryte(n: int) -> tuple[str, str, str]:
    n %= 27
    r0 = n % 3
    r1 = (n // 3) % 3
    r2 = (n // 9) % 3
    return (RES_TO_TRIT[r2], RES_TO_TRIT[r1], RES_TO_TRIT[r0])

def trits_to_trytes(trits: str) -> list[int]:
    if len(trits) % 3 != 0:
        raise ValueError("Trit string length must be multiple of 3")
    out = []
    for i in range(0, len(trits), 3):
        out.append(tryte_from_trits(trits[i], trits[i+1], trits[i+2]))
    return out

def trytes_to_trits(trytes: list[int]) -> str:
    chars = []
    for n in trytes:
        t2, t1, t0 = trits_from_tryte(n)
        chars.extend([t2, t1, t0])
    return ''.join(chars)

# ----------------------------
# GF(3) and GF(3^3) arithmetic
# Field: F3[x]/(x^3 + 2x + 1)
# ----------------------------

def gf3_add(a: int, b: int) -> int: return (a + b) % 3
def gf3_mul(a: int, b: int) -> int: return (a * b) % 3

def gf33_int_to_coeffs(a: int) -> tuple[int, int, int]:
    a %= 27
    return (a % 3, (a // 3) % 3, (a // 9) % 3)

def gf33_coeffs_to_int(a0: int, a1: int, a2: int) -> int:
    return (a0 % 3) + 3 * (a1 % 3) + 9 * (a2 % 3)

def gf33_add(a: int, b: int) -> int:
    a0,a1,a2 = gf33_int_to_coeffs(a)
    b0,b1,b2 = gf33_int_to_coeffs(b)
    return gf33_coeffs_to_int(gf3_add(a0,b0), gf3_add(a1,b1), gf3_add(a2,b2))

def gf33_neg(a: int) -> int:
    a0,a1,a2 = gf33_int_to_coeffs(a)
    return gf33_coeffs_to_int((-a0) % 3, (-a1) % 3, (-a2) % 3)

def gf33_sub(a: int, b: int) -> int:
    return gf33_add(a, gf33_neg(b))

def gf33_mul(a: int, b: int) -> int:
    a0,a1,a2 = gf33_int_to_coeffs(a)
    b0,b1,b2 = gf33_int_to_coeffs(b)

    d0 = gf3_mul(a0, b0)
    d1 = (gf3_mul(a0, b1) + gf3_mul(a1, b0)) % 3
    d2 = (gf3_mul(a0, b2) + gf3_mul(a1, b1) + gf3_mul(a2, b0)) % 3
    d3 = (gf3_mul(a1, b2) + gf3_mul(a2, b1)) % 3
    d4 = gf3_mul(a2, b2)

    if d4 != 0:
        d2 = (d2 + d4) % 3
        d1 = (d1 + 2*d4) % 3
        d4 = 0
    if d3 != 0:
        d1 = (d1 + d3) % 3
        d0 = (d0 + 2*d3) % 3
        d3 = 0

    return gf33_coeffs_to_int(d0, d1, d2)

def gf33_is_zero(a: int) -> bool:
    return a % 27 == 0

def gf33_inv(a: int) -> int:
    a %= 27
    if gf33_is_zero(a):
        raise ZeroDivisionError("No inverse of zero in GF(3^3).")
    for b in range(1, 27):
        if gf33_mul(a, b) == 1:
            return b
    raise RuntimeError("No inverse found")

def gf33_pow(a: int, e: int) -> int:
    a %= 27
    if e < 0:
        a = gf33_inv(a); e = -e
    result, base = 1, a
    while e > 0:
        if e & 1:
            result = gf33_mul(result, base)
        base = gf33_mul(base, base)
        e >>= 1
    return result % 27

# ----------------------------
# S-box and inverse
# ----------------------------

SBOX_C0 = 1
SBOX_A  = gf33_coeffs_to_int(1, 1, 0)  # 1 + x
SBOX_B  = gf33_coeffs_to_int(2, 1, 0)  # 2 + x
SBOX_A_INV = gf33_inv(SBOX_A)

def sbox(x: int) -> int:
    x %= 27
    if gf33_is_zero(x):
        return SBOX_C0
    inv = gf33_inv(x)
    t = gf33_mul(SBOX_A, inv)
    return gf33_add(t, SBOX_B) % 27

def inv_sbox(y: int) -> int:
    y %= 27
    if y == SBOX_C0:
        return 0
    temp = gf33_sub(y, SBOX_B)
    if gf33_is_zero(temp):
        raise RuntimeError("Invalid S-box output for inverse.")
    z = gf33_mul(SBOX_A_INV, temp)
    return gf33_inv(z) % 27

def subtrytes_state(state: list[list[int]]) -> None:
    for r in range(3):
        for c in range(12):
            state[r][c] = sbox(state[r][c])

def inv_subtrytes_state(state: list[list[int]]) -> None:
    for r in range(3):
        for c in range(12):
            state[r][c] = inv_sbox(state[r][c])

# ----------------------------
# ShiftRows / InvShiftRows
# ----------------------------

def shiftrows_state(state: list[list[int]]) -> None:
    for r in range(3):
        row = state[r]
        s = r % 12
        if s:
            state[r] = row[s:] + row[:s]

def inv_shiftrows_state(state: list[list[int]]) -> None:
    for r in range(3):
        row = state[r]
        s = r % 12
        if s:
            state[r] = row[-s:] + row[:-s]

# ----------------------------
# MixColumns / InvMixColumns
# ----------------------------

ALPHA = gf33_coeffs_to_int(0, 1, 0)  # x

MIX_MAT = [
    [1,     ALPHA, 1],
    [1,     1,     ALPHA],
    [ALPHA, 1,     1],
]

def mat_vec_mul_3x3(M: list[list[int]], v: list[int]) -> list[int]:
    r = [0, 0, 0]
    for i in range(3):
        acc = 0
        for j in range(3):
            acc = gf33_add(acc, gf33_mul(M[i][j], v[j]))
        r[i] = acc % 27
    return r

def mix_single_column(col: list[int]) -> list[int]:
    return mat_vec_mul_3x3(MIX_MAT, col)

def inv_matrix_3x3(M: list[list[int]]) -> list[list[int]]:
    A = [[M[i][j] for j in range(3)] for i in range(3)]
    Inv = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    for col in range(3):
        pivot = col
        while pivot < 3 and gf33_is_zero(A[pivot][col]):
            pivot += 1
        if pivot == 3:
            raise RuntimeError("Matrix not invertible")
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            Inv[col], Inv[pivot] = Inv[pivot], Inv[col]
        pv = A[col][col]
        inv_pv = gf33_inv(pv)
        for j in range(3):
            A[col][j] = gf33_mul(A[col][j], inv_pv)
            Inv[col][j] = gf33_mul(Inv[col][j], inv_pv)
        for r in range(3):
            if r == col:
                continue
            f = A[r][col]
            if gf33_is_zero(f):
                continue
            for j in range(3):
                A[r][j] = gf33_sub(A[r][j], gf33_mul(f, A[col][j]))
                Inv[r][j] = gf33_sub(Inv[r][j], gf33_mul(f, Inv[col][j]))
    return Inv

MIX_INV_MAT = inv_matrix_3x3(MIX_MAT)

def mixcolumns_state(state: list[list[int]]) -> None:
    for c in range(12):
        col = [state[r][c] for r in range(3)]
        m = mix_single_column(col)
        for r in range(3):
            state[r][c] = m[r]

def inv_mixcolumns_state(state: list[list[int]]) -> None:
    for c in range(12):
        col = [state[r][c] for r in range(3)]
        m = mat_vec_mul_3x3(MIX_INV_MAT, col)
        for r in range(3):
            state[r][c] = m[r]

# ----------------------------
# AddRoundKey
# ----------------------------

def addroundkey_state(state: list[list[int]], round_key: list[list[int]]) -> None:
    for r in range(3):
        for c in range(12):
            state[r][c] = gf33_add(state[r][c], round_key[r][c])

# ----------------------------
# Key schedule
# ----------------------------

NB = 12  # state columns
NK = 18  # key columns
NR = 10  # rounds

def rotword(col: list[int]) -> list[int]:
    return [col[1], col[2], col[0]]

def subword(col: list[int]) -> list[int]:
    return [sbox(x) for x in col]

def rcon_column(round_index: int) -> list[int]:
    rc_val = gf33_pow(ALPHA, round_index - 1)
    return [rc_val, 0, 0]

def key_schedule(key_trytes: list[int]) -> list[list[list[int]]]:
    if len(key_trytes) != 54:
        raise ValueError("key_trytes must have length 54 (162 trits).")

    W: list[list[int]] = []
    for i in range(NK):
        base = 3 * i
        W.append([key_trytes[base], key_trytes[base+1], key_trytes[base+2]])

    total_words = (NR + 1) * NB

    for i in range(NK, total_words):
        temp = W[i - 1].copy()
        if i % NK == 0:
            temp = rotword(temp)
            temp = subword(temp)
            rc = rcon_column(i // NK)
            temp = [gf33_add(t, r) for t, r in zip(temp, rc)]
        prev = W[i - NK]
        W.append([gf33_add(p, t) for p, t in zip(prev, temp)])

    round_keys: list[list[list[int]]] = []
    for r in range(NR + 1):
        rk = [[0]*NB for _ in range(3)]
        for c in range(NB):
            word = W[r*NB + c]
            for row in range(3):
                rk[row][c] = word[row]
        round_keys.append(rk)

    return round_keys

# ----------------------------
# Block mapping: trits <-> state
# ----------------------------

def trits_to_state(trits: str) -> list[list[int]]:
    if len(trits) != 108:
        raise ValueError("Block must be exactly 108 trits.")
    trytes = trits_to_trytes(trits)
    if len(trytes) != 36:
        raise RuntimeError("Internal length mismatch.")
    state = [[0]*NB for _ in range(3)]
    for c in range(NB):
        for r in range(3):
            idx = 3*c + r
            state[r][c] = trytes[idx]
    return state

def state_to_trits(state: list[list[int]]) -> str:
    trytes: list[int] = []
    for c in range(NB):
        for r in range(3):
            trytes.append(state[r][c])
    return trytes_to_trits(trytes)

# ----------------------------
# Block cipher: encrypt/decrypt 108-trit block
# ----------------------------

def encrypt_block(plaintext_trits: str, key_trits: str) -> str:
    if len(plaintext_trits) != 108:
        raise ValueError("Plaintext must be 108 trits.")
    if len(key_trits) != 162:
        raise ValueError("Key must be 162 trits.")

    key_trytes = trits_to_trytes(key_trits)
    round_keys = key_schedule(key_trytes)
    state = trits_to_state(plaintext_trits)

    addroundkey_state(state, round_keys[0])

    for rnd in range(1, NR):
        subtrytes_state(state)
        shiftrows_state(state)
        mixcolumns_state(state)
        addroundkey_state(state, round_keys[rnd])

    subtrytes_state(state)
    shiftrows_state(state)
    addroundkey_state(state, round_keys[NR])

    return state_to_trits(state)

def decrypt_block(ciphertext_trits: str, key_trits: str) -> str:
    if len(ciphertext_trits) != 108:
        raise ValueError("Ciphertext must be 108 trits.")
    if len(key_trits) != 162:
        raise ValueError("Key must be 162 trits.")

    key_trytes = trits_to_trytes(key_trits)
    round_keys = key_schedule(key_trytes)
    state = trits_to_state(ciphertext_trits)

    addroundkey_state(state, round_keys[NR])

    for rnd in range(NR-1, 0, -1):
        inv_shiftrows_state(state)
        inv_subtrytes_state(state)
        addroundkey_state(state, round_keys[rnd])
        inv_mixcolumns_state(state)

    inv_shiftrows_state(state)
    inv_subtrytes_state(state)
    addroundkey_state(state, round_keys[0])

    return state_to_trits(state)

# ----------------------------
# Bytes <-> balanced trits (6 trits per byte)
# (use ONLY for plaintext / recovered data, not arbitrary ciphertext)
# ----------------------------

def byte_to_trits(b: int) -> str:
    if not (0 <= b <= 255):
        raise ValueError("Byte must be in 0..255")
    digits = [0] * 6
    n = b
    for i in range(5, -1, -1):
        digits[i] = n % 3
        n //= 3
    return ''.join(RES_TO_TRIT[d] for d in digits)

def trits_to_byte(trits: str) -> int:
    if len(trits) != 6:
        raise ValueError("Need exactly 6 trits to form a byte.")
    digits = [TRIT_TO_RES[c] for c in trits]
    n = 0
    for d in digits:
        n = n*3 + d
    if not (0 <= n <= 255):
        raise RuntimeError("Decoded value out of byte range; encoding mismatch.")
    return n

def bytes_to_trits(data: bytes) -> str:
    return ''.join(byte_to_trits(b) for b in data)

def trits_to_bytes(trits: str) -> bytes:
    if len(trits) % 6 != 0:
        raise ValueError("Trit string length must be multiple of 6.")
    out = []
    for i in range(0, len(trits), 6):
        out.append(trits_to_byte(trits[i:i+6]))
    return bytes(out)

# ----------------------------
# PACK / UNPACK arbitrary trit strings to bytes
# (ciphertext-safe, uses base-3 <-> base-256 with 4-byte length header)
# ----------------------------

def pack_trits_to_bytes(trits: str) -> bytes:
    """
    Pack an arbitrary-length balanced trit string into bytes.
    Format:
        [4-byte big-endian trit_length] [base-256 representation of value]
    where value is the base-3 integer defined by the trits (0,1,2 residues).
    """
    length = len(trits)
    n = 0
    for ch in trits:
        n = n * 3 + TRIT_TO_RES[ch]
    payload = bytearray()
    if n == 0:
        payload_bytes = b""
    else:
        while n > 0:
            payload.append(n & 0xFF)
            n >>= 8
        payload_bytes = bytes(reversed(payload))
    length_header = length.to_bytes(4, "big")
    return length_header + payload_bytes

def unpack_bytes_to_trits(data: bytes) -> str:
    """
    Reverse of pack_trits_to_bytes.
    Takes bytes in the format:
        [4-byte length][payload]
    and returns the original balanced-trit string.
    """
    if len(data) < 4:
        raise ValueError("Packed data too short to contain length header.")
    length = int.from_bytes(data[:4], "big")
    payload = data[4:]
    n = 0
    for b in payload:
        n = (n << 8) + b
    trits = ['0'] * length
    for i in range(length - 1, -1, -1):
        trits[i] = RES_TO_TRIT[n % 3]
        n //= 3
    if n != 0:
        raise ValueError("Packed data is inconsistent with length header.")
    return ''.join(trits)

# ----------------------------
# CTR mode over trits
# ----------------------------

def int_to_fixed_trits(n: int, length: int) -> str:
    """
    Encode non-negative integer n into exactly `length` trits (unbalanced residues),
    then map 0->'0',1->'1',2->'T'.
    """
    if n < 0:
        raise ValueError("Counter/nonce must be non-negative")
    digits = [0] * length
    i = length - 1
    x = n
    while i >= 0:
        digits[i] = x % 3
        x //= 3
        i -= 1
    if x != 0:
        raise ValueError("Value too large to fit in given trit length")
    return ''.join(RES_TO_TRIT[d] for d in digits)

def encrypt_ctr_trits(plaintext_trits: str, key_trits: str,
                      nonce: int, initial_counter: int = 0) -> str:
    """
    CTR mode on arbitrary-length trit string.
    keystream_block = E_key( counter_block )
    ciphertext = plaintext (+) keystream (mod 3, balanced)
    """
    if len(key_trits) != 162:
        raise ValueError("Key must be 162 trits.")
    out = []
    idx = 0
    block_index = 0
    while idx < len(plaintext_trits):
        block_len = min(108, len(plaintext_trits) - idx)
        counter_val = nonce + initial_counter + block_index
        counter_trits = int_to_fixed_trits(counter_val, 108)
        keystream = encrypt_block(counter_trits, key_trits)
        for j in range(block_len):
            out.append(trit_add_char(plaintext_trits[idx + j], keystream[j]))
        idx += block_len
        block_index += 1
    return ''.join(out)

def decrypt_ctr_trits(ciphertext_trits: str, key_trits: str,
                      nonce: int, initial_counter: int = 0) -> str:
    """
    CTR decryption over ternary:
        P = C - K  (mod 3)
    where K is the keystream generated exactly as in encryption.
    """
    if len(key_trits) != 162:
        raise ValueError("Key must be 162 trits.")
    out = []
    idx = 0
    block_index = 0
    while idx < len(ciphertext_trits):
        block_len = min(108, len(ciphertext_trits) - idx)
        counter_val = nonce + initial_counter + block_index
        counter_trits = int_to_fixed_trits(counter_val, 108)
        keystream = encrypt_block(counter_trits, key_trits)
        for j in range(block_len):
            out.append(trit_sub_char(ciphertext_trits[idx + j], keystream[j]))
        idx += block_len
        block_index += 1
    return ''.join(out)

# ----------------------------
# Byte-level CTR helpers (packed ciphertext bytes)
# ----------------------------

def encrypt_ctr_bytes(plaintext: bytes, key_bytes: bytes,
                      nonce: int, initial_counter: int = 0) -> bytes:
    """
    Encrypt arbitrary-length plaintext bytes with a 27-byte key.
    Returns ciphertext as packed bytes (length header + base-256 ternary payload).
    """
    if len(key_bytes) != 27:
        raise ValueError("Key must be exactly 27 bytes (162 trits).")
    pt_trits = bytes_to_trits(plaintext)
    key_trits = bytes_to_trits(key_bytes)
    ct_trits = encrypt_ctr_trits(pt_trits, key_trits, nonce, initial_counter)
    return pack_trits_to_bytes(ct_trits)

def decrypt_ctr_bytes(ciphertext_bytes: bytes, key_bytes: bytes,
                      nonce: int, initial_counter: int = 0) -> bytes:
    """
    Decrypt packed ciphertext bytes produced by encrypt_ctr_bytes.
    Returns the original plaintext bytes.
    """
    if len(key_bytes) != 27:
        raise ValueError("Key must be exactly 27 bytes (162 trits).")
    key_trits = bytes_to_trits(key_bytes)
    ct_trits = unpack_bytes_to_trits(ciphertext_bytes)
    pt_trits = decrypt_ctr_trits(ct_trits, key_trits, nonce, initial_counter)
    return trits_to_bytes(pt_trits)

# ----------------------------
# MAC / AEAD support
# ----------------------------

def _pad_trits_1zero(message_trits: str, block_size: int = 108) -> str:
    """
    Simple '1 followed by zeros' padding:
        M_padded = M || '1' || '0'... so that len(M_padded) is a multiple of block_size.
    This encodes the length and removes ambiguity.
    """
    padded = message_trits + '1'
    while len(padded) % block_size != 0:
        padded += '0'
    return padded

def mac_cbc_trits(message_trits: str, key_trits: str) -> str:
    """
    CBC-MAC–style MAC over trits:
        state_0 = 0^block
        state_i = E_k( state_{i-1} + M_i )
    where + is ternary add, and M_i are 108-trit blocks of padded message.
    Returns a 108-trit MAC tag.
    """
    if len(key_trits) != 162:
        raise ValueError("MAC key must be 162 trits.")
    block_size = 108
    state = '0' * block_size
    padded = _pad_trits_1zero(message_trits, block_size)
    for i in range(0, len(padded), block_size):
        block = padded[i:i+block_size]
        x = trit_add_block(state, block)
        state = encrypt_block(x, key_trits)
    return state  # 108 trits

def constant_time_equal(a: bytes, b: bytes) -> bool:
    """
    Constant-time comparison of two byte strings.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0

def compute_mac_bytes(associated_data: bytes, ciphertext_bytes: bytes,
                      nonce: int, mac_key_bytes: bytes) -> bytes:
    """
    Compute a MAC tag over (associated_data, nonce, ciphertext_bytes)
    using CBC-MAC over trits with the ternary block cipher.

    Input MAC key is 27 bytes (162 trits). Output tag is packed ternary bytes.
    """
    if len(mac_key_bytes) != 27:
        raise ValueError("MAC key must be exactly 27 bytes (162 trits).")
    if nonce < 0 or nonce >= (1 << 64):
        raise ValueError("Nonce must fit in 64 bits for MAC encoding.")
    nonce_bytes = nonce.to_bytes(8, "big")

    header = (
        len(associated_data).to_bytes(4, "big") +
        len(ciphertext_bytes).to_bytes(4, "big")
    )
    message_bytes = header + nonce_bytes + associated_data + ciphertext_bytes

    message_trits = bytes_to_trits(message_bytes)
    key_trits = bytes_to_trits(mac_key_bytes)
    tag_trits = mac_cbc_trits(message_trits, key_trits)
    return pack_trits_to_bytes(tag_trits)

def encrypt_aead_bytes(plaintext: bytes,
                       enc_key_bytes: bytes,
                       mac_key_bytes: bytes,
                       nonce: int,
                       associated_data: bytes = b"",
                       initial_counter: int = 0) -> tuple[bytes, bytes]:
    """
    AEAD-style authenticated encryption (Encrypt-then-MAC).

    - enc_key_bytes: 27-byte key for CTR encryption.
    - mac_key_bytes: 27-byte key for CBC-MAC.
    - nonce: integer (<= 2^64-1) shared between encryption and MAC.
    - associated_data: additional authenticated data (AAD), not encrypted.

    Returns:
        (ciphertext_bytes, tag_bytes)
    """
    ciphertext_bytes = encrypt_ctr_bytes(plaintext, enc_key_bytes, nonce, initial_counter)
    tag_bytes = compute_mac_bytes(associated_data, ciphertext_bytes, nonce, mac_key_bytes)
    return ciphertext_bytes, tag_bytes

def decrypt_aead_bytes(ciphertext_bytes: bytes,
                       tag_bytes: bytes,
                       enc_key_bytes: bytes,
                       mac_key_bytes: bytes,
                       nonce: int,
                       associated_data: bytes = b"",
                       initial_counter: int = 0) -> bytes:
    """
    AEAD decryption / verification.

    Raises ValueError if authentication fails.
    """
    expected_tag = compute_mac_bytes(associated_data, ciphertext_bytes, nonce, mac_key_bytes)
    if not constant_time_equal(expected_tag, tag_bytes):
        raise ValueError("Authentication failed (tag mismatch).")
    return decrypt_ctr_bytes(ciphertext_bytes, enc_key_bytes, nonce, initial_counter)

# ----------------------------
# CLI
# ----------------------------

def _parse_nonce(s: str) -> int:
    """
    Parse nonce string as int, accepting decimal or 0x-prefixed hex.
    """
    s = s.strip()
    if s.lower().startswith("0x"):
        return int(s, 16)
    return int(s, 10)

def main_cli() -> None:
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(
        description="Balanced-ternary AEAD cipher (Terncrypt: encrypt/decrypt/gen-keys)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Encrypt command
    enc = sub.add_parser("encrypt", help="Encrypt a file")
    enc.add_argument("-i", "--input", required=True, help="Input plaintext file")
    enc.add_argument("-o", "--output", required=True, help="Output ciphertext file")
    enc.add_argument("-t", "--tag-output", required=True, help="Output tag file")
    enc.add_argument("-k", "--enc-key", required=True, help="Encryption key file (27 bytes)")
    enc.add_argument("-m", "--mac-key", required=True, help="MAC key file (27 bytes)")
    enc.add_argument("-n", "--nonce", required=True,
                     help="Nonce (integer, decimal or 0xHEX)")
    enc.add_argument("-a", "--aad", help="Associated data file (optional)")

    # Decrypt command
    dec = sub.add_parser("decrypt", help="Decrypt a file")
    dec.add_argument("-i", "--input", required=True, help="Input ciphertext file")
    dec.add_argument("-t", "--tag", required=True, help="Input tag file")
    dec.add_argument("-o", "--output", required=True, help="Output plaintext file")
    dec.add_argument("-k", "--enc-key", required=True, help="Encryption key file (27 bytes)")
    dec.add_argument("-m", "--mac-key", required=True, help="MAC key file (27 bytes)")
    dec.add_argument("-n", "--nonce", required=True,
                     help="Nonce (integer, decimal or 0xHEX)")
    dec.add_argument("-a", "--aad", help="Associated data file (optional)")

    # Gen-keys command
    gen = sub.add_parser("gen-keys", help="Generate a new encryption + MAC key pair")
    gen.add_argument("-k", "--enc-key-out", required=True,
                     help="Output file for encryption key (27 random bytes)")
    gen.add_argument("-m", "--mac-key-out", required=True,
                     help="Output file for MAC key (27 random bytes)")
    gen.add_argument("-f", "--force", action="store_true",
                     help="Overwrite existing key files without prompting")

    args = parser.parse_args()

    def read_file(path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    def write_file(path: str, data: bytes, *, overwrite: bool = True) -> None:
        if not overwrite and os.path.exists(path):
            raise FileExistsError(f"Refusing to overwrite existing file: {path}")
        with open(path, "wb") as f:
            f.write(data)

    if args.command == "encrypt":
        nonce = _parse_nonce(args.nonce)
        pt = read_file(args.input)
        enc_key = read_file(args.enc_key)
        mac_key = read_file(args.mac_key)
        aad = read_file(args.aad) if args.aad else b""

        try:
            ct_bytes, tag_bytes = encrypt_aead_bytes(pt, enc_key, mac_key, nonce, aad)
        except Exception as e:
            print(f"[!] Encryption failed: {e}", file=sys.stderr)
            sys.exit(1)

        write_file(args.output, ct_bytes)
        write_file(args.tag_output, tag_bytes)
        print(f"[+] Encrypted {len(pt)} bytes -> {len(ct_bytes)}-byte ciphertext")
        print(f"[+] Tag length: {len(tag_bytes)} bytes")
        print(f"[+] Ciphertext written to: {args.output}")
        print(f"[+] Tag written to       : {args.tag_output}")

    elif args.command == "decrypt":
        nonce = _parse_nonce(args.nonce)
        ct_bytes = read_file(args.input)
        tag_bytes = read_file(args.tag)
        enc_key = read_file(args.enc_key)
        mac_key = read_file(args.mac_key)
        aad = read_file(args.aad) if args.aad else b""

        try:
            pt = decrypt_aead_bytes(ct_bytes, tag_bytes, enc_key, mac_key, nonce, aad)
        except Exception as e:
            print(f"[!] Decryption failed: {e}", file=sys.stderr)
            sys.exit(1)

        write_file(args.output, pt)
        print(f"[+] Decrypted to {len(pt)} bytes")
        print(f"[+] Plaintext written to: {args.output}")

    elif args.command == "gen-keys":
        enc_path = args.enc_key_out
        mac_path = args.mac_key_out
        force = args.force

        # Basic safety: don't overwrite unless -f/--force is given
        if not force:
            for p in (enc_path, mac_path):
                if os.path.exists(p):
                    print(f"[!] {p} already exists. Use -f/--force to overwrite.", file=sys.stderr)
                    sys.exit(1)

        enc_key = os.urandom(27)
        mac_key = os.urandom(27)

        try:
            write_file(enc_path, enc_key, overwrite=True)
            write_file(mac_path, mac_key, overwrite=True)
        except Exception as e:
            print(f"[!] Failed to write keys: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"[+] Generated encryption key (27 bytes) -> {enc_path}")
        print(f"[+] Generated MAC key        (27 bytes) -> {mac_path}")


def main() -> None:
    """Console entry point for the 'terncrypt' command."""
    main_cli()
