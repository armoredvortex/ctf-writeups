---
title: Home
layout: home
permalink: /
---

# My CTF Writeups Collection

This site documents my journey through various Capture The Flag (CTF) challenges and platforms.

## Latest Writeups

{% for post in site.posts limit:5 %}

- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%Y-%m-%d" }}
  {% endfor %}
