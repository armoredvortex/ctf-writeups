---
title: "GDB baby step 2"
date: 2025-05-09
layout: writeup
platform: picoGym
categories: [Reverse Engineering]
tags: [gdb, assembly]
challenge_link: https://play.picoctf.org/practice/challenge/396
---

# GDB baby step 2

## Challenge Description

We're asked to figure out the value inside `eax` register at the end of `main` function.
Flag format is `picoCTF{n}` where n is the decimal value inside the register.

## Disassembling the binary

```nasm
(gdb) disas main
Dump of assembler code for function main:
   0x0000000000401106 <+0>:	endbr64
   0x000000000040110a <+4>:	push   %rbp
   0x000000000040110b <+5>:	mov    %rsp,%rbp
   0x000000000040110e <+8>:	mov    %edi,-0x14(%rbp)
   0x0000000000401111 <+11>:	mov    %rsi,-0x20(%rbp)
   0x0000000000401115 <+15>:	movl   $0x1e0da,-0x4(%rbp)
   0x000000000040111c <+22>:	movl   $0x25f,-0xc(%rbp)
   0x0000000000401123 <+29>:	movl   $0x0,-0x8(%rbp)
   0x000000000040112a <+36>:	jmp    0x401136 <main+48>
   0x000000000040112c <+38>:	mov    -0x8(%rbp),%eax
   0x000000000040112f <+41>:	add    %eax,-0x4(%rbp)
   0x0000000000401132 <+44>:	addl   $0x1,-0x8(%rbp)
   0x0000000000401136 <+48>:	mov    -0x8(%rbp),%eax
   0x0000000000401139 <+51>:	cmp    -0xc(%rbp),%eax
   0x000000000040113c <+54>:	jl     0x40112c <main+38>
   0x000000000040113e <+56>:	mov    -0x4(%rbp),%eax
   0x0000000000401141 <+59>:	pop    %rbp
   0x0000000000401142 <+60>:	ret
End of assembler dump.
```

We can analyze this code and try to figure out the value inside `eax` register at the end of `main` function, or simply we can set a breakpoint at the end of `main` function and run the program until it hits the breakpoint.

```nasm
(gdb) break *0x401142
Breakpoint 1 at 0x401142
(gdb) run
Starting program: /home/armoredvortex/Downloads/debugger0_b
(gdb) info registers
rax            0x4af4b             307019
...
```

## Solution

Flag is just the decimal value of `0x4af4b`

```python
print('picoCTF{' + str(0x4af4b) + '}')
```
