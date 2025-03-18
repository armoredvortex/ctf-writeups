---
title: "Permissions"
date: 2025-03-17
layout: writeup
platform: picoGym
categories: [Reverse Engineering]
tags: [permissions, sudo, vi, hidden-files]
difficulty: Easy
---

# Permissions

## Challenge Description

Challenge title says permissions and we do not have perms to read /root.

## Checking Sudo Privileges

Do we have sudo? Yes.

Running `sudo -l` reveals we have sudo perms for vi.

## Attempting to Access the Flag

Running `sudo vi /root/flag.txt` results in nothing!

## Exploring the /root Directory

Maybe the flag is under a different name.

Running `sudo vi /root`, we see in the file explorer `.flag.txt` (a hidden file).

## Retrieving the Flag

Opening it reveals the flag.
