---
title: "Naughty Cat"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Forensics]
tags: [zip, john]
difficulty: Easy
---

# Naughty Cat

## Challenge Description

We're given a zip file and the prompt says "Can you _crack_ open the mystery", which might just mean we need to brute force the password.

Since there wasn't any other information, I believed this was the right approach.

## Solution

```bash
$ zip2john secret.zip > hash.txt
$ john --wordlist=/usr/share/wordlists/seclists/Passwords/Leaked-Databases/rockyou.txt hash.txt
$ john --show hash.txt

```

This gave me the password `trustno1`.
Opening the zip file gave me an image with the flag.

`saic{f1n4lly_y0u_c4p7ur3d_m3_h1dd3n!!}`
