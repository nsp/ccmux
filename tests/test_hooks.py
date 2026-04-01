from ccmux.hooks import generate_hook_script, get_hooks_config


def test_generate_start_hook():
    script = generate_hook_script("SessionStart")
    assert "#!/bin/bash" in script
    assert "ccmux agent-event start" in script
    assert "session_id" in script
    assert "ghostty" in script.lower() or "osascript" in script


def test_generate_stop_hook():
    script = generate_hook_script("SessionEnd")
    assert "#!/bin/bash" in script
    assert "ccmux agent-event stop" in script


def test_hooks_config_format():
    config = get_hooks_config()
    assert "hooks" in config
    assert "SessionStart" in config["hooks"]
    assert "SessionEnd" in config["hooks"]


def test_install_hooks(tmp_path, monkeypatch):
    from ccmux.hooks import install_hooks, HOOKS_DIR
    monkeypatch.setattr("ccmux.hooks.HOOKS_DIR", tmp_path / "hooks")

    created = install_hooks()
    assert len(created) == 2
    for path in created:
        assert path.exists()
        content = path.read_text()
        assert "#!/bin/bash" in content
