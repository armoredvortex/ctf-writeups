---
title: "transformation"
date: 2025-03-18
layout: writeup
platform: picoGym
categories: [Reverse Engineering]
tags: [ascii, utf, python]
difficulty: Easy
---

# Transformation

## Challenge Description

We're given python code that transforms the flag.
`''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])`

## Inspecting the output

The output is a string of characters that look like Chinese or Japanese (I'm not sure).
As far as I know these characters take up two bytes instead of the usual one byte.

## Analyzing the code

The code takes two characters at a time, converts them to their ASCII values, shifts the first character by 8 bits and adds the second character to it.

Let's take the first two characters of our flag 'pi'.

`(ord('p') << 8) + ord('i') = 112 << 8 + 105 = 28777`

112 in binary is `01110000` and 105 in binary is `01101001`.

So our output becomes `0111000001101001` which is the binary representation of 28777.

The ASCII value of 28777 is `瑩`.

## Solution

```python
f = open('enc', 'r')
s = f.read()

for c in s:
  i = ord(c)
  a = i >> 8
  b = i%(1<<8)
  print(chr(a), end='')
  print(chr(b), end='')
```
