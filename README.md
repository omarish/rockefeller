# John D. Rockefeller's Dotfiles?

What would John D. Rockefeller's dotfiles look like?

Engineers can learn to be capitalists. One part of this is through automation.

This repo is a collection of tools to make you a more productive engineer, manager, CEO, and allocator of capital.

## Status

None of this works yet, but PRs are welcome if this project resonates and you'd like to contribute.

## Current Functionality

| Task                | Entrypoint  |
| ------------------- | ----------- |
| Manage gmail labels | In progress |


```sh
git clone https://github.com/omarish/rockefeller.git
cd rockefeller
uv install
```

## gmail

### `upsert-labels`

Programmatically manage your gmail labels.

```
uv run python3 -m rockefeller.cli gmail upsert-labels john.d.rockefeller@gmail.com --from-file=data/john.d.rockefeller@gmail.com-labels.json
```