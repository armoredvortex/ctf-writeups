---
title: "FalseStart"
date: 2025-03-29
layout: writeup
platform: chronosCTF 2025
categories: [Web]
tags: [Next.js, JWT]
difficulty: Medium
---

# False Start

## Challenge Description

We're given a Next.js application with authentication. The goal is to access the `/flag` page, but it requires an admin session.

The challenge provides a login route that sets an authentication token as an HTTP-only cookie.

## JWT

seeing a JWT implementation, I thought about forging a token.
The `generateAuthToken` function uses `HS256` with a secret from `process.env.AUTH_TOKEN`.

But later I realised that it is not possible to forge it without the knowledge of the secret.

## Next.js Middleware Bypass

I figured that the application uses Next.js middleware for authentication. The middleware checks if the user is an admin and redirects to the `/flag` page if they are.

This is a very popular recent vulnerability found in Next.js.
[Refer](https://youtu.be/AaCnBOqyvIM?si=F6u5v4GZFRV05ZiA)

I opened burp suite and intercepted the request to the `/flag` endpoint.
Then I added the vulnerable header.

<img src="{{ 'assets/images/FalseStart/burp.png' | relative_url }}" alt="headers"/>
```
X-Middleware-Subrequest: src/middleware:src/middleware:src/middleware:src/middleware:src/middleware
```

`saic{1t_w4s_N3v3r_4b0ut_th3_JWT}`
