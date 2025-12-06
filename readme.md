Terncrypt
A balanced-ternary AEAD cipher and command-line encryption tool

Terncrypt is an experimental balanced-ternary authenticated encryption algorithm implemented in Python.
It uses a custom AES-style block cipher operating on 108-trit blocks, combined with CTR mode and a ternary CBC-MAC to provide AEAD (authenticated encryption with associated data).

Unlike binary ciphers, Terncrypt operates entirely on balanced ternary digits:

-1 → T
 0 → 0
+1 → 1


Although this system is mathematically interesting and fully functional, it is not intended for production-grade security. It is a research toy, a cryptographic art project, and a demonstration of what encryption might look like in a ternary computing world.

🚀 Features
✔ Balanced-ternary symmetric block cipher

108-trit block size

162-trit key (27 bytes → 162 trits)

AES-inspired structure (SubTrytes → ShiftRows → MixColumns → AddRoundKey)

S-Box defined via multiplicative inversion in GF(3³)

Diffusion via a 3×3 matrix over GF(3³)

Full key schedule (18 tryte words → 198 expanded words)

✔ AEAD mode (Encrypt-then-MAC)

Encryption: CTR mode over trits

Authentication: CBC-MAC over trits

Associated data (AAD) support

Tamper detection via constant-time MAC comparison

✔ Fully pip-installable Python package

Organized with:

pyproject.toml
src/terncrypt/

✔ Clean, user-friendly CLI

After install:

terncrypt encrypt ...
terncrypt decrypt ...
terncrypt gen-keys ...

✔ Binary-safe ciphertext format

Ternary ciphertext is packed using:

4-byte length header

Base-3 → base-256 conversion

Makes ciphertext compact and portable.

📦 Installation
Install from a local checkout
pip install -e .


(Use py -m pip on Windows if needed.)

After install, the following command becomes available:
terncrypt

🔐 Key Generation

Terncrypt uses two keys, each 27 bytes long:

Encryption key (CTR mode)

MAC key (CBC-MAC)

Generate both:

terncrypt gen-keys -k enc.key -m mac.key


Overwrite existing files safely:

terncrypt gen-keys -k enc.key -m mac.key -f

🔒 Encryption
terncrypt encrypt \
  -i plaintext.bin \
  -o ciphertext.tenc \
  -t ciphertext.tag \
  -k enc.key \
  -m mac.key \
  -n 12345 \
  -a optional_aad.bin


ciphertext.tenc contains the packed ternary ciphertext

ciphertext.tag contains the authentication tag

The nonce must be reused for decryption

AAD is authenticated but not encrypted

🔓 Decryption
terncrypt decrypt \
  -i ciphertext.tenc \
  -t ciphertext.tag \
  -o recovered.bin \
  -k enc.key \
  -m mac.key \
  -n 12345 \
  -a optional_aad.bin


If the tag does not match:

[!] Authentication failed (tag mismatch)


Terncrypt never outputs plaintext on MAC failure.

🧠 Balanced Ternary Overview

Balanced ternary uses the digits:

Value	Trit
-1	T
0	0
+1	1

Arithmetic is performed modulo 3, mapping T → 2, 1 → 1, 0 → 0.

This makes ternary addition analogous to XOR in binary ciphers—but with three possible states instead of two.

Terncrypt internally represents trytes as elements of GF(3³), allowing full S-box and MixColumns operations analogous to AES but over a ternary field.

🧮 Cipher Overview
Block size

108 trits → 36 trytes → 3×12 matrix of GF(3³) elements

Key size

162 trits → 54 trytes

Round function
state = AddRoundKey(state, round_keys[0])

for r = 1..9:
    state = SubTrytes(state)
    state = ShiftRows(state)
    state = MixColumns(state)
    state = AddRoundKey(state, round_keys[r])

Final round:
    state = SubTrytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, round_keys[10])

AEAD mode outline
ciphertext = CTR(key_enc, nonce, plaintext)
tag = CBC-MAC(key_mac, AAD || nonce || ciphertext)

⚠️ Security Notes

Terncrypt is not intended for real-world cryptographic security.

It has not been analyzed by cryptographers and should not be used to protect sensitive data.

Reasons:

Novel balanced-ternary S-box may have exploitable structure

Round count (10) chosen for experimentation, not proven security

Field GF(3³) operations haven't undergone cryptanalysis

CBC-MAC construction is simple and works but isn’t hardened

Side-channel resistance not considered

This project is meant as:

a cryptographic research toy

an educational demonstration

an experiment in ternary computation

🧪 Example: Encrypting a file
terncrypt gen-keys -k enc.key -m mac.key

terncrypt encrypt \
  -i image.jpg \
  -o image.jpg.tenc \
  -t image.jpg.tag \
  -k enc.key \
  -m mac.key \
  -n 42


Decryption:

terncrypt decrypt \
  -i image.jpg.tenc \
  -t image.jpg.tag \
  -o image_recovered.jpg \
  -k enc.key \
  -m mac.key \
  -n 42

🛠 Development

Install dev copy:

pip install -e .


Run tests (if we build you a test suite):

pytest

📄 License

MIT License (or any license you choose — let me know if you want me to draft one).

🙌 Credits

Terncrypt was created as an exploration into:

balanced ternary arithmetic

AES-style cipher design in a non-binary domain

experimenting with GF(3³) substitution and diffusion

constructing a full ternary AEAD pipeline