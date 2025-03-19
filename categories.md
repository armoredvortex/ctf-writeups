---
layout: default
title: Categories
permalink: /categories/
---

# Writeups by Category

{% for category in site.categories %}

## {{ category[0] }}

{% for post in category[1] %}

- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%Y-%m-%d" }}
  {% endfor %}

{% endfor %}
