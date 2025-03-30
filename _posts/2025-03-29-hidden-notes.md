---
title: "Hidden Notes"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Forensics]
tags: [hexdump, xxd, audio]
difficulty: Easy
---

# Hidden Notes

## Challenge Description

We're given a file called `esrcte.awv` and the prompt says "Can you tune in and uncover what’s hidden?"

## Observations

The file extension `.awv` is an anagram of `.wav`, and the filename `esrcte` is an anagram of `secret`.

I tried playing the file, but it didn't work.
I checked the file type using `file` command, and it said it couldn't recognize the file type.

I used `xxd` to view the file in hex format, and I noticed that the first 4 bytes were `0x49 0x52 0x46 0x46`, which is the ASCII representation of `IRFF`.
The format for a wav file is supposed to be `RIFF`, so I used `hexedit` to fix the magic bytes but it still didnt work when I tried to play it.

That is when I realised that the shuffling followed a pattern.
For the filename, every two bytes were swapped, so in the file, every two bytes must've been swapped too.

## Solution

```python
with open('esrcte.awv', 'rb') as f:
    data = f.read()
swapped_data = swap_adjacent_bytes(data)
with open('secret.wav', 'wb') as f:
    f.write(swapped_data)

def swap_adjacent_bytes(data: bytes) -> bytes:
    swapped = bytearray(data)
    for i in range(0, len(swapped) - 1, 2):
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
    return bytes(swapped)
```

Running spectrogram on the file revealed the flag.

<img src="{{ 'assets/images/hidden-notes/spectrogram.png' | relative_url }}" alt="SPECTOGRAM"/>

`saic{h1dd3n_n0735_4r3_10ud357}`
