---
title: "OSINT ChronosCTF 2025"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [OSINT]
tags: [osint]
---

# Writeups for all the OSINT challenges I solved in ChronosCTF 2025

# Back In Time - 1 (Welcome)

## Solution

Pretty simple challenge. The flag was in the Welcome tab of the ChronosCTF website.
`SAIC{w3lc0m3_t0_chr0n0s_ctf_2025}`

# Back In Time - 2

## Challenge Description

The challenge mentioned a traitor who was a member of the SAIC team, but has been removed now.

## Solution

I visited the SAIC website and checked the team page.

The prompt mentioned that the traitor was removed, so I checked the `Wayback Machine` for the SAIC team page.

There was a previous snapshot of the page which contained an extra member named `"Pavitr Prabhakar"`.

Opening their github page, the flag was in their profile `README`.
`saic{p@v1tr_g0t_c4ugh7_1n_w4yb4ck_w3b!!}`

# Back In Time - 3

## Challenge Description

There was a Github repo called `Back-In-Time-III` with a password locked zip file.

## Solution

Looking at the previous commits, There was a commit called `Delete FLAG.pff`.
Opening the file, There were two pieces of information.

I couldn't understand the first line, but the second line looked like a hash.
Looking up the hash on Crackstation, I got `Straczynski`.

Luckily enough, that was the password for the zip file.
I unzipped the file and got a file called `flag.txt` with the flag inside.
`saic{c3wl_w0rd5_f0r_bru73f0rc1ng!!}`

# Back In Time - 4

## Challenge Description

The prompt mentioned "A fragment of leaked information has surfaced—hidden in the depths of the internet. It contains _pasted_ clues about our ex-member’s online presence."

And it also said that they might've changed usernames.

## Solution

I tried looking up the username `pavitr-saic` on pastebin but it wasn't there.

The profile README on the Github account mentioned `"I'm Pavitr Prabhakar aka SpideyPavitr!"`
So I tried looked up `SpideyPavitr` on pastebin and found a paste with the flag inside.

`saic{pu61ic_p4st3_pr1v4t3_l055}`
