---
title: "Tiny, But Secure?"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Reverse Engineering]
tags: [iso]
difficulty: Easy
---

# Tiny, But Secure?

## Challenge Description

We're given a tinycore iso file and the prompt says "Maybe there’s some secret deep inside. See if you can find something in the roots."

## Mounting the ISO

I started by mounting the ISO file to see its contents. I used the following command:

```bash
$ sudo mount -o loop tinycore.iso /mnt
```

This command mounts the ISO file to the `/mnt` directory. After mounting, I navigated to the `/mnt` directory to explore its contents.

```bash
$ ls /mnt
boot
$ ls boot
core.gz  isolinux  vmlinuz
```

## Solution

I copied over and unzipped the `core.gz` file:

```bash
$ cp /mnt/boot/core.gz /tmp
$ cd /tmp
$ gzip -d core.gz
$ ls
core
$ file core
core: ASCII cpio archive (SVR4 with no CRC)
$ cpio -id < ./core
```

And then I got a lot of files. I looked for files inside the root directory and found a file called `secret` with the flag inside.

`saic{you_found_the_core}`
