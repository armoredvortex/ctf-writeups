---
title: "Two Time Pad"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Cryptography]
tags: [crypto, aes]
difficulty: Hard
---

# Two Time Pad

## Challenge Description

We were given a Python script `source.py` that encrypts a secret message containing a flag, and the resulting ciphertext `out.txt`.

## Understanding the Encryption

The secret message `Everything is .. saic{--REDACTED--}` is converted into hex. And it creates a dictionary `encoding` which creates a unique very long (768 bytes!) block of data for each possible hex character.

Let's call this the "base block" for that character.

This step is fixed – the base block for 'a' is always the same, the base block for 'b' is always the same, etc., but they are different from each other.

## XOR + AES

The block_xor function goes through our `encoding` dictionary and, and generates a new random 16 bytes key everytime. It them scrambles our 768 byte base block with the key.

Finally, it encrypts the result with AES in ECB mode.

## Solution

I thought since the base blocks were the same for the characters then even after the XOR scrambling and the final AES ECB encryption, the pattern or signature of their corresponding 768-byte ciphertext chunks should be identical.

The script below, reads ciphertext and splits it into chunks.

It then calculates the signature for each of them and builds a map (signature->character)

Then finally it loops through all the chunk signatures and looks up that signature in the map.

```python
B_SIZE = 16
B_CNT = 48
CHUNK_SIZE = B_SIZE * B_CNT
BLOCK_SIZE = B_SIZE

def get_chunk_signature(chunk_bytes):
    blocks = []
    for i in range(B_CNT):
        block = chunk_bytes[i * BLOCK_SIZE : (i + 1) * BLOCK_SIZE]
        blocks.append(block)
    mapping = {}
    signature = []
    next_id = 0
    for block in blocks:
        if block not in mapping:
            mapping[block] = next_id
            next_id += 1
        signature.append(mapping[block])
    return tuple(signature)

with open("out.txt", "rb") as f:
    ciphertext = f.read()
print(f"{len(ciphertext)} bytes")

NUM_CHUNKS = len(ciphertext) // CHUNK_SIZE
print(f"{NUM_CHUNKS} hex characters.")

# calculating signatures
signatures = []
for i in range(NUM_CHUNKS):
    chunk = ciphertext[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
    sig = get_chunk_signature(chunk)
    signatures.append(sig)

M_known_prefix = "Everything is coincidence. But even coincidence is part of fate's design. Anyways, here is the flag - saic{"
DATA_known_prefix_hex = M_known_prefix.encode().hex()
prefix_len = len(DATA_known_prefix_hex)

signature_to_char = {}

for i in range(prefix_len):
    char = DATA_known_prefix_hex[i]
    sig = signatures[i]

    if sig not in signature_to_char:
        signature_to_char[sig] = char

num_unique_signatures = len(signature_to_char)

decoded_hex_list = []
for i in range(NUM_CHUNKS):
    sig = signatures[i]
    decoded_hex_list.append(signature_to_char[sig])

decoded_hex = "".join(decoded_hex_list)

print(bytes.fromhex(decoded_hex))
```

`saic{Wh0s3_Ey35_aR3_7h0se_3y35?--fun^10xint^40=Ir2}`
