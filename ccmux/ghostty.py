"""Ghostty terminal UUID retrieval via AppleScript."""

import os
import subprocess
from typing import Optional


APPLESCRIPT = (
    'tell application "Ghostty" to get id of focused terminal '
    'of selected tab of front window'
)


def get_ghostty_uuid() -> Optional[str]:
    """Get the UUID of the focused Ghostty terminal tab.

    Returns None if not running in Ghostty or if the query fails.
    """
    if os.environ.get("TERM_PROGRAM", "").lower() != "ghostty":
        return None

    try:
        result = subprocess.run(
            ["osascript", "-e", APPLESCRIPT],
            capture_output=True,
            text=True,
            check=True,
            timeout=2,
        )
        uuid = result.stdout.strip()
        return uuid if uuid else None
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None
