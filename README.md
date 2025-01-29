# John D. Rockefeller's Dotfiles

I want to prove that I can be both a great engineer and also a great capital allocator.

One part of this is through automation of daily tasks. Streamlining the things that take up previous time.

This repo is a collection of tools that I use (or want to use) to make my life more streamlined, efficient, and complete.

It's hard to answer what constitutes a complete life, but I'm pretty sure it does not involve manually managing gmail labels. Or doing these mundane things that we think we should do but don't need to.

## Status

None of this works yet, but PRs are welcome if this project resonates and you'd like to contribute. I'm currently building my company (https://center.app) but this is something that I'll add to whenever I can.

## Current Functionality

| Task                | Entrypoint        |
| ------------------- | ----------------- |
| Manage gmail labels | WIP (not working) |


## Setup

```sh
git clone https://github.com/omarish/rockefeller.git
cd rockefeller
uv install
```

## `gmail`

### `upsert-labels`

Use case: you're working with an excellent EA and you want to manage your labels to streamline inbox management. Except they have access to all 10 of your email addresses. Use this to streamline label management across gmail inboxes.

```
uv run python3 -m rockefeller.cli gmail upsert-labels john.d.rockefeller@gmail.com --from-file=data/john.d.rockefeller@gmail.com-labels.json
```

## Other notes

This is my first time using `uv` for python package management, so I'd appreciate any suggestions on how to streamline the developer experience.