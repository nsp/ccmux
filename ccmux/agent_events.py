"""Process lifecycle events from Claude Code agent hooks."""

from datetime import datetime, timezone
from typing import Optional

from ccmux import state
from ccmux.exceptions import SessionNotFoundError
from ccmux.session_layout import notify_sidebars


def process_agent_event(
    claude_session_id: str,
    event: str,
    ghostty_uuid: Optional[str] = None,
    status: Optional[str] = None,
    activity: Optional[str] = None,
) -> str:
    """Process a lifecycle event from a Claude Code hook.

    Returns the ccmux session name that was updated.
    Raises SessionNotFoundError if no session matches.
    """
    found = state.find_session_by_claude_id(claude_session_id)
    if not found:
        raise SessionNotFoundError(
            f"claude_session_id={claude_session_id}",
            "Session may not have been created via ccmux.",
        )
    session_name, _ = found

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    updates: dict = {"agent_updated_at": now}

    if event == "start":
        updates["agent_status"] = "running"
        if ghostty_uuid:
            updates["ghostty_uuid"] = ghostty_uuid
    elif event == "stop":
        updates["agent_status"] = "detached"
    elif event == "activity":
        if status:
            updates["agent_status"] = status
        if activity:
            updates["agent_activity"] = activity

    state.update_session(session_name, **updates)
    notify_sidebars()
    return session_name
