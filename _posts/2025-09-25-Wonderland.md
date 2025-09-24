---
title: "Wonderland"
date: 2025-09-25
layout: writeup
platform: TryHackMe
categories: [web, pentesting, linux, boot2root]
tags: [web, pentesting, linux, boot2root]
---

# Wonderland

Writeup for the Wonderland room on TryHackMe.

## Enumeration

We start with a simple nmap scan which shows that there is an `http` server running on the target.

Using `gobuster` we we find an endpoint `/r` which looks interesting.
Visiting it tells us to "Keep going forward".
So i run `gobuster` again and find another endpoint `/r/a`.
With the same message.

The first page told us to look for a white rabbit. So its trivial to guess that the next endpoint is `/r/a/b` and so on...

On the `r/a/b/b/i/t` endpoint we're told to open the door and enter the wonderland.

The webpage sourcecode contans credentials for a user `alice:HowDothTheLittleCrocodileImproveHisShiningTail`

## Alice

Using the credentials we found we can login to alice user.
There is a python script which we cannot modify.

However `sudo -l` shows that we can run the python script as `rabbit` user.
Since we cannot modify the script, we can override the python import of the `random` module.

To do this I simply create a file named `random.py` with a reverse shell payload.
Then I run the python script with `sudo -u rabbit /usr/bin/python3 /home/alice/walrus_and_the_carpenter.py`

And I get a shell as `rabbit` user.

## Rabbit

In rabbit's home directory there is a suid binary called `teaParty`.
Running the binary gives some time and date as output, reads a character from stdin and then segfaults.

To analyze this binary I copied it over to my system using a simple python http server.

Then I open the binary in binaryninja.

```
setuid(uid: 0x3eb)
setgid(gid: 0x3eb)
puts(str: "Welcome to the tea party!\nThe Mad Hatter will be here soon.")
004011a0        system(line: "/bin/echo -n 'Probably by ' && date --date='next hour' -R")
puts(str: "Ask very nicely, and I will give you some tea while you wait for him")
getchar()
return puts(str: "Segmentation fault (core dumped)")
```

The binary sets its uid and gid to hatter and executes a system command to print the date of the next hour.

The binary doesn't pass the absolute path to `date` so we can create our own malicious script called `date` and just modify the `PATH` env variable.

`export PATH=/tmp` and we create the `date` script in `/tmp` which just spawns a reverse shell.

## Hatter

Now we need to finally get to `root` user.
I started looking around but didn't really find anything interesting.

This is when linpeas came in handy.

Under the Capabilities section it found something interesting.

```
/usr/bin/perl = cap_setuid+ep
```

This means that the perl binary can use the `setuid()` system call.
So after a quick google search I found that we can use perl to spawn a shell as any user.

```
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
```

And we get a root shell.
