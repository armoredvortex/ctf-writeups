---
title: "endianness"
date: 2025-03-18
layout: writeup
platform: picoGym
categories: [Reverse Engineering]
tags: [endianness, little-endian, big-endian]
difficulty: Easy
---

# Endianness

## Challenge Description

We're given a string and asked to find out the little endian and big endian notation
Inspecting the source, we see that we have to enter the hex values.

## Endianness Explained

Looking up wikipedia, I found this neat diagram that explains it well.

<img src="{{ 'assets/images/endianness/endianness.jpg' | relative_url }}" alt="Endianness" class="post-content" />

## Solution

Let's say the string is 'wbjzs'

### Little Endian:

```python
s = 'wbjzs'
reversed_s = ''.join(reversed(s))
print(bytes.hex(reversed_s.encode()))
```

### Big Endian:

```python
s = 'wbjzs'
print(bytes.hex(s.encode()))
```

### Flag

Entering the hex values in the prompt returns back the flag.
