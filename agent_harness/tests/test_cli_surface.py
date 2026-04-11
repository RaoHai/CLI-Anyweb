"""CLI tests for the direct agent-browser style command surface."""

import json
from unittest.mock import patch

from click.testing import CliRunner

from agent_harness.gui_agent_harness_cli import cli


class TestDirectCommands:
    """Test the flat top-level command aliases."""

    def setup_method(self):
        from agent_harness import gui_agent_harness_cli as cli_mod

        cli_mod._session = None
        cli_mod._json_output = False
        cli_mod._repl_mode = False
        cli_mod._availability_cached = (True, "agent-browser ok")

    def test_open_command_uses_page_module(self):
        runner = CliRunner()
        with patch("agent_harness.gui_agent_harness_cli.page_mod.open_page") as mock_open:
            mock_open.return_value = {"url": "https://example.com", "status": "loaded"}

            result = runner.invoke(cli, ["open", "https://example.com"])

            assert result.exit_code == 0
            mock_open.assert_called_once()
            assert "Opened: https://example.com" in result.output

    def test_snapshot_command_prints_snapshot_text(self):
        runner = CliRunner()
        with patch("agent_harness.gui_agent_harness_cli.backend.snapshot") as mock_snapshot:
            mock_snapshot.return_value = {"snapshot": "- document \"Example\"", "refs": {}}

            result = runner.invoke(cli, ["snapshot"])

            assert result.exit_code == 0
            assert "- document \"Example\"" in result.output

    def test_get_command_json_output(self):
        runner = CliRunner()
        with patch("agent_harness.gui_agent_harness_cli.backend.get_value") as mock_get:
            mock_get.return_value = {"field": "url", "value": "https://example.com"}

            result = runner.invoke(cli, ["--json", "get", "url"])

            assert result.exit_code == 0
            data = json.loads(result.output)
            assert data["value"] == "https://example.com"

    def test_find_command_prints_matches(self):
        runner = CliRunner()
        with patch("agent_harness.gui_agent_harness_cli.backend.find") as mock_find:
            mock_find.return_value = {"query": "login", "matches": ["/main/button[0]"], "count": 1}

            result = runner.invoke(cli, ["find", "login"])

            assert result.exit_code == 0
            assert "Matches for 'login':" in result.output
            assert "/main/button[0]" in result.output

    def test_click_command_uses_backend(self):
        runner = CliRunner()
        with patch("agent_harness.gui_agent_harness_cli.backend.click") as mock_click:
            mock_click.return_value = {"action": "click", "path": "/main/button[0]", "status": "success"}

            result = runner.invoke(cli, ["click", "@12"])

            assert result.exit_code == 0
            mock_click.assert_called_once_with("@12", use_daemon=False)

    def test_type_command_uses_backend(self):
        runner = CliRunner()
        with patch("agent_harness.gui_agent_harness_cli.backend.type_text") as mock_type:
            mock_type.return_value = {"action": "type", "path": "/main/input[0]", "status": "success"}

            result = runner.invoke(cli, ["type", "@15", "hello"])

            assert result.exit_code == 0
            mock_type.assert_called_once_with("@15", "hello", use_daemon=False)

    def test_legacy_group_commands_are_not_exposed(self):
        runner = CliRunner()

        result = runner.invoke(cli, ["page", "open", "https://example.com"])

        assert result.exit_code != 0
        assert "No such command 'page'" in result.output
