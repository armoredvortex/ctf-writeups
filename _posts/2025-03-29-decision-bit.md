---
title: "Decision-Bit"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Cryptography]
tags: []
difficulty: Easy
---

# Decision-Bit Write Up

## Challenge Prompt

Someone tried to be clever and hid the flag… by randomly throwing away some of it! Now all that’s left are some numbers and a bunch of "X"s. Can you put the pieces back together and recover what they tried to erase?

# Solution Walkthrough

We were given a python script and its output when it was run on the flag. On opening the script, we can understand that the script first converted the entire flag into binary and wherever there was a '1' it replaced it with an X and wherever there was a '0' it replaced it with a random number.

The python script converts the Xs into 1s and anything else to 0.

```python
from Crypto.Util.number import long_to_bytes

with open("output(1).txt", "r") as f:
    output = [line.strip() for line in f.readlines()]

bin_flag = "".join("1" if x == "X" else "0" for x in output)

flag = long_to_bytes(int(bin_flag, 2))

print("flag:", flag.decode())
```

`saic{ch3ck_t0rsion_aft3r_pa1ring}`
