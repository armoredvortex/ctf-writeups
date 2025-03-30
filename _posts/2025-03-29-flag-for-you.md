---
title: "Flag for you"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Miscellaneous]
tags: []
difficulty: Easy
---

# Flag for you

## Challenge Description

We're provided with a file `flag.txt` that contains ascii art of a flag.

## Solution

Scanning line by line we can see that the letters of the flag format `saic{` are randomly scattered in the ascii art.
We can extract the letters and form the flag.

```python
with open('flag.txt', 'r') as f:
    content = f.read()

for c in content:
    if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}":
        print(c, end='')
```

`saic{S4IC_1S_4W3S0M3}`
