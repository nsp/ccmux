import pytest
from unittest.mock import patch

from ccmux.agent_events import process_agent_event
from ccmux.exceptions import SessionNotFoundError


@patch("ccmux.agent_events.notify_sidebars")
def test_start_event_updates_status(mock_notify, tmp_path, monkeypatch):
    monkeypatch.setattr("ccmux.state.store.STATE_FILE", tmp_path / "state.json")
    monkeypatch.setattr("ccmux.state.store.STATE_DIR", tmp_path)

    from ccmux.state import store
    store.add_session("fox", "/repo", "/repo/wt", claude_session_id="uuid-123")

    process_agent_event(
        claude_session_id="uuid-123",
        event="start",
        ghostty_uuid="GHOST-ABC",
    )

    sess = store.get_session("fox")
    assert sess.agent_status == "running"
    assert sess.ghostty_uuid == "GHOST-ABC"
    assert sess.agent_updated_at is not None
    mock_notify.assert_called_once()


@patch("ccmux.agent_events.notify_sidebars")
def test_stop_event_marks_detached(mock_notify, tmp_path, monkeypatch):
    monkeypatch.setattr("ccmux.state.store.STATE_FILE", tmp_path / "state.json")
    monkeypatch.setattr("ccmux.state.store.STATE_DIR", tmp_path)

    from ccmux.state import store
    store.add_session("fox", "/repo", "/repo/wt", claude_session_id="uuid-123")

    process_agent_event(claude_session_id="uuid-123", event="stop")

    sess = store.get_session("fox")
    assert sess.agent_status == "detached"


@patch("ccmux.agent_events.notify_sidebars")
def test_activity_event_updates_fields(mock_notify, tmp_path, monkeypatch):
    monkeypatch.setattr("ccmux.state.store.STATE_FILE", tmp_path / "state.json")
    monkeypatch.setattr("ccmux.state.store.STATE_DIR", tmp_path)

    from ccmux.state import store
    store.add_session("fox", "/repo", "/repo/wt", claude_session_id="uuid-123")

    process_agent_event(
        claude_session_id="uuid-123",
        event="activity",
        status="waiting_input",
        activity="Permission prompt: Edit file.py",
    )

    sess = store.get_session("fox")
    assert sess.agent_status == "waiting_input"
    assert sess.agent_activity == "Permission prompt: Edit file.py"


@patch("ccmux.agent_events.notify_sidebars")
def test_unknown_session_raises(mock_notify, tmp_path, monkeypatch):
    monkeypatch.setattr("ccmux.state.store.STATE_FILE", tmp_path / "state.json")
    monkeypatch.setattr("ccmux.state.store.STATE_DIR", tmp_path)

    with pytest.raises(SessionNotFoundError):
        process_agent_event(claude_session_id="nonexistent", event="start")
