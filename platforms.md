---
layout: default
title: Platforms
permalink: /platforms/
---

# Writeups by Platform

{% assign platforms = site.posts | map: 'platform' | uniq | sort %}

{% for platform in platforms %}

## {{ platform }}

{% assign posts_in_platform = site.posts | where: "platform", platform %}
{% for post in posts_in_platform %}

- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y-%m-%d" }}
  {% endfor %}

{% endfor %}
