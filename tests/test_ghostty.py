import subprocess
from unittest.mock import patch

from ccmux.ghostty import get_ghostty_uuid


def test_returns_uuid_when_ghostty_available(monkeypatch):
    monkeypatch.setenv("TERM_PROGRAM", "ghostty")
    with patch("ccmux.ghostty.subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout="50451542-E7C4-4377-8F12-D1858F7E8DEA\n",
        )
        result = get_ghostty_uuid()
        assert result == "50451542-E7C4-4377-8F12-D1858F7E8DEA"


def test_returns_none_when_ghostty_not_available(monkeypatch):
    monkeypatch.setenv("TERM_PROGRAM", "ghostty")
    with patch("ccmux.ghostty.subprocess.run", side_effect=subprocess.CalledProcessError(1, "osascript")):
        result = get_ghostty_uuid()
        assert result is None


def test_returns_none_when_not_ghostty_terminal(monkeypatch):
    monkeypatch.setenv("TERM_PROGRAM", "iTerm2")
    result = get_ghostty_uuid()
    assert result is None


def test_returns_none_on_timeout(monkeypatch):
    monkeypatch.setenv("TERM_PROGRAM", "ghostty")
    with patch("ccmux.ghostty.subprocess.run", side_effect=subprocess.TimeoutExpired("osascript", 2)):
        result = get_ghostty_uuid()
        assert result is None
