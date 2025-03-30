---
title: "Challenge Response"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Cryptography]
tags: [sha, hashlib]
difficulty: Easy
---

# Challenge Response

## Challenge Description

We're given a server to connect to, and the [source]({{ 'assets/scripts/challenge-response/server.py' | relative_url }}).
The server generates a `admin_hash` with the admin password and a random salt.

I found this challenge extremely poorly written, The vulnerability is written in plain sight in comments.

```python
# Vulnerability: if the client sends the special byte 0x7f, leak the admin hash and session salt
if b'\x7f' in data:
    leak = f"admin: {admin_hash}\nSecret salt: '{session_salt}'\n".encode()
    conn.sendall(leak)
    continue
```

## Solution

I connected to the server and sent the special byte `0x7f` to leak the admin hash and session salt.

```python
c = remote('url_goes_here', port)
c.read()
c.send(b"\x7f\n")
response = conn.recvuntil(b">>> ").decode()
print("Leaked data:", response)
```

The server responds with the admin hash and session salt.
Now it expects me to send the hash of the admin hash with the session salt for some reason to reveal the flag as mentioned in the source.

```python
if data == b'1':
    conn.sendall(b"username: ")
    username = conn.recv(1024).strip().decode()
    if username != "admin":
        conn.sendall(b"Only admin login is supported.\n")
        continue
    # For admin login, generate a new login salt
    login_salt = generate_salt(32)
    prompt = f"Compute hash(admin_hash + '{login_salt}'): ".encode()
    conn.sendall(prompt)
    user_hash = conn.recv(1024).strip().decode()
    expected = secret_hash(admin_hash, login_salt)
    if user_hash == expected:
        conn.sendall(f"Access granted. Flag: {FLAG}\n".encode())
    else:
        conn.sendall(b"Access denied.\n")
```

So that was fairly easy!

```python
import hashlib
def secret_hash(s, salt):
    return hashlib.sha3_256((s + salt).encode()).hexdigest()

admin_hash = "admin_hash_goes_here"
login = "login_salt_goes_here"

print(secret_hash(admin_hash, login_salt))
```

Sending the hash to the server reveals the flag.

`saic{s0m3tim3s_7he_h4sh_is_ju57_as_v@lu4bl3_45_7h3_p4ssw0rd!}`
