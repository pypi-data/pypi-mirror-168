"""Logging handling."""
import sys
from datetime import datetime

import click


def warn(msg: str):
    """Emit a warning message."""
    click.secho(fmt(msg), err=True, fg="yellow")


def debug(msg: str):
    """Emit a debug message."""
    state = get_state()
    if state.debug:
        click.secho(fmt(msg), fg="cyan")


def error(msg: str, exit: bool = True):
    """Emit an error message."""
    click.secho(fmt(msg), err=True, fg="red")
    if exit:
        sys.exit(1)


def fmt(msg: str) -> str:
    time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    return f"[{time}] BACorakel {msg}"


def get_state():
    from bacorakel.state import state

    return state
