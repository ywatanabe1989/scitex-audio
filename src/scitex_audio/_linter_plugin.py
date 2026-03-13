#!/usr/bin/env python3
"""Linter plugin for scitex-audio (scitex_linter.plugins entry point)."""


def get_plugin():
    """Return linter plugin configuration for scitex-audio.

    Returns empty plugin for now — audio rules can be added later.
    """
    return {
        "rules": [],
        "call_rules": {},
        "axes_hints": {},
        "checkers": [],
    }


# EOF
