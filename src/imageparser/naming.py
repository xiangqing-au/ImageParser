"""Helpers for analysis input names and screenshot paths."""

from __future__ import annotations

import os

_APP_PREFIXES = ("BOLT_", "INDRIVE_", "GOOGLE_")


def get_city_path(name: str) -> str:
    """Strip a legacy app prefix to get the route-file name (``BOLT_NYC`` -> ``NYC``)."""
    for prefix in _APP_PREFIXES:
        if name.startswith(prefix):
            return name[len(prefix):]
    return name


def screenshot_path(folder: str, city: str, date: str, route_id: int, suffix: str) -> str:
    """Build the canonical screenshot file path ``<city><date><id:03d><suffix>.png``."""
    return os.path.join(folder, f"{city}{date}{route_id:03d}{suffix}.png")
