---
title: "No-HashCat"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Miscellaneous]
tags: [hashcat, john]
difficulty: Medium
---

# No Hash Cat

## Challenge Description

We're given a password hash and are asked to crack it.
The challenge mentions that the password also has the "static" parts of the flag.

Which means we probably have to brute force `saic{...}`.
Researching the hash type, I found out that it is a yescrypt hash.

## Solution

```bash
$ echo "$y$j9T$s/UaF7EiN0ylLVryw75Co1$6WdEcyhcU.f8Fa/HhKBHCPC7qUN3fSxbNR3izAHNvE6" > hash.txt

$ john --mask='saic{?w}' --wordlist=/usr/share/wordlists/seclists/Passwords/Leaked-Databases/rockyou.txt --format=crypt hash.txt

$ john --show hash.txt
```

Reveals the flag.
`saic{backstreetboys}`
