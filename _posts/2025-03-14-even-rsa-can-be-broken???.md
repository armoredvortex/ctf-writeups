---
title: "EVEN RSA can be broken???"
date: 2025-03-14
layout: writeup
platform: picoCTF 2025
categories: [Cryptography]
tags: [RSA, Factorization]
challenge_link: https://play.picoctf.org/practice/challenge/470
---

# EVEN RSA can be broken???

## Challenge Description

Upon connecting to the netcat session, we're given a public key, and an encrypted message.

```yaml
N: 16375465040134266382037924142261457528501112186543277792848630721807078306485077249619287137402110974899308506833533987056612232484498384265166192025834658
e: 65537
cyphertext: 9384788041067957192357453688593182889705957211944894943414722698189021872249952206507140260400308242509220300272796981273284608421792186869677424904909493
```

## RSA Background

RSA uses to large prime numbers `p` and `q` to generate the public and private keys.
The public key is `(N, e)` and the private key is `(N, d)` where `d` is the modular multiplicative inverse of `e` modulo `(p-1)(q-1)`.

where N = p \* q

## Vulnerability

RSA relies on the fact that it is computationally infeasible to factorize the product of two large prime numbers.

However just by looking at our value of N, we can tell that its an even number and one of its factor is 2.

## Solution

I used sagemath to solve this.

```python
from Crypto.Util.number import long_to_bytes
N = 16375465040134266382037924142261457528501112186543277792848630721807078306485077249619287137402110974899308506833533987056612232484498384265166192025834658
e = 65537
cyphertext = 9384788041067957192357453688593182889705957211944894943414722698189021872249952206507140260400308242509220300272796981273284608421792186869677424904909493

p = 2
q = N/2
d = inverse_mod(e, (p-1)*(q-1))
m = pow(cyphertext, d, N)
print(long_to_bytes(m))
```
