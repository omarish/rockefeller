#!/usr/bin/env python3
import typer
from typing import Optional

from . import gmail

app = typer.Typer(
    help="Rockefeller: a Python toolset for automation and streamlining tasks."
)
app.add_typer(gmail.app, name="gmail")


# Sub-app for Gmail operations
def main():
    app()


if __name__ == "__main__":
    main()
