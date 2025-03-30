---
title: "RSARSARSA"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Cryptography]
tags: [RSA, CRT]
difficulty: Medium
---

# RSARSARSA

## Challenge Description

We're given a python script that generates 3 public keys and encrypts a message using them.

```python
def generate_tripled_rsa(flag, bits=1024, e=3):

    m = bytes_to_long(flag.encode())
    n1 = generate_rsa_key(bits)
    n2 = generate_rsa_key(bits)
    n3 = generate_rsa_key(bits)

    c1 = pow(m, e, n1)
    c2 = pow(m, e, n2)
    c3 = pow(m, e, n3)

    return (n1, c1), (n2, c2), (n3, c3)

(n1, c1), (n2, c2), (n3, c3) = generate_tripled_rsa(flag, bits=1024, 3)
```

And we're given the output of the script.

```
n1 = 181374681834993...
c1 = 112614359142069...
n2 = 267411241009182...
c2 = 112614359142069...
n3 = 196649862823757...
c3 = 112614359142069...
```

## Solution

I noticed that the ciphertexts are the same, and the moduli are different.
This means that we can use the Chinese Remainder Theorem (CRT) to solve for the plaintext.
The CRT states that if we have a system of congruences:

```
x ≡ a1 (mod n1)
x ≡ a2 (mod n2)
x ≡ a3 (mod n3)

# where x = m^e
# and a1 = a2 = a3 = c
```

For our case, since all the ciphertexts are the same, it means m^e is smaller than all of the moduli.

I used sagemath to compute the cuberoot of the ciphertext.

```python
from Crypto.Util.number import long_to_bytes

c1 = 112614359142069...
m_long = int(c1.nth_root(3))
m = long_to_bytes(m_long)
print(m)
```

`saic{my_7r1pp3ll3d_RSA_D!D_n07_Co0k}`
