---
title: "GDB baby step 1"
date: 2025-03-18
layout: writeup
platform: picoGym
categories: [Reverse Engineering]
tags: [gdb, assembly]
challenge_link: https://play.picoctf.org/practice/challenge/395
---

# GDB baby step 1

## Challenge Description

We're asked to figure out the value inside `eax` register at the end of `main` function.
Flag format is `picoCTF{n}` where n is the decimal value inside the register.

## Disassembling the binary

```nasm
(gdb) disas main
Dump of assembler code for function main:
   0x0000555555555129 <+0>:	endbr64
   0x000055555555512d <+4>:	push   %rbp
   0x000055555555512e <+5>:	mov    %rsp,%rbp
   0x0000555555555131 <+8>:	mov    %edi,-0x4(%rbp)
   0x0000555555555134 <+11>:	mov    %rsi,-0x10(%rbp)
   0x0000555555555138 <+15>:	mov    $0x86342,%eax
   0x000055555555513d <+20>:	pop    %rbp
=> 0x000055555555513e <+21>:	ret
End of assembler dump.
```

We can see that the value `0x86342` is moved into `eax` register.

## Solution

Flag is just the decimal value of `0x86342`

```python
print('picoCTF{' + str(0x86342) + '}')
```
