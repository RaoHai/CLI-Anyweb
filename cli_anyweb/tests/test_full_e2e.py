"""E2E tests for cli-anyweb.

These tests interact with a real browser via agent-browser.

Usage:
    python -m pytest cli_anyweb/tests/test_full_e2e.py -v
"""

import os
import pytest
from click.testing import CliRunner

from cli_anyweb.utils.agent_browser_backend import is_available
from cli_anyweb.cli_anyweb_cli import cli

# Control whether to run browser E2E tests via an environment variable.
# This avoids invoking the external CLI during test collection
# in environments that have not explicitly opted in.
AGENT_BROWSER_E2E_ENABLED = os.environ.get("AGENT_BROWSER_E2E", "").lower() in {"1", "true", "yes"}

# Skip all tests if E2E is not enabled or agent-browser is not available.
# `is_available()` is only called when AGENT_BROWSER_E2E_ENABLED is true.
pytestmark = pytest.mark.skipif(
    (not AGENT_BROWSER_E2E_ENABLED) or (not is_available()[0]),
    reason=(
        "agent-browser E2E tests are disabled or agent-browser is not available. "
        "Set AGENT_BROWSER_E2E=1 to enable and ensure agent-browser is installed."
    ),
)

TEST_URL = "https://example.com"


@pytest.fixture
def runner():
    return CliRunner()


class TestDependencyChecks:
    """Test that dependency checking works correctly."""

    def test_cli_starts_when_backend_available(self, runner):
        """CLI should start successfully when agent-browser is available."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "cli-anyweb" in result.output or "web automation" in result.output.lower()


class TestPageCommands:
    """Test page navigation commands."""

    def test_page_info_empty(self, runner):
        """Page info shows empty state initially."""
        result = runner.invoke(cli, ["--json", "info"])
        assert result.exit_code == 0
        import json
        data = json.loads(result.output)
        assert data["url"] == "(no page loaded)"
        assert data["working_dir"] == "/"


class TestFilesystemCommands:
    """Test filesystem commands."""

    def test_fs_pwd(self, runner):
        """Print working directory shows root initially."""
        result = runner.invoke(cli, ["pwd"])
        assert result.exit_code == 0
        assert result.output.strip() == "/"


class TestSessionCommands:
    """Test session management commands."""

    def test_session_status(self, runner):
        """Session status shows current state."""
        result = runner.invoke(cli, ["--json", "status"])
        assert result.exit_code == 0
        import json
        data = json.loads(result.output)
        assert "current_url" in data
        assert "working_dir" in data


class TestDaemonMode:
    """Test daemon mode functionality."""

    @pytest.mark.manual
    def test_daemon_lifecycle(self, runner):
        """Manual test: Start daemon, run commands, stop daemon.

        To run manually:
            cli-anyweb daemon-start
            cli-anyweb pwd
            cli-anyweb daemon-stop
        """
        pass

    def test_daemon_start_with_json(self, runner):
        """Daemon start returns success in JSON."""
        result = runner.invoke(cli, ["--json", "daemon-start"])
        # May fail if daemon can't start, but should return JSON
        assert result.exit_code == 0
        import json
        data = json.loads(result.output)
        assert "daemon" in data or "error" in data


class TestErrorHandling:
    """Test error handling for edge cases."""

    def test_invalid_path_gives_error(self, runner):
        """Invalid path should give clear error."""
        # Note: This test's behavior depends on agent-browser's error handling
        result = runner.invoke(cli, ["cd", "/invalid/path/that/does/not/exist"])
        # Should not crash; exit code may be 0 or 1 depending on error handling
        assert result.exception is None
        assert result.exit_code in (0, 1)

    def test_empty_page_info(self, runner):
        """Page info with no page loaded shows empty state."""
        result = runner.invoke(cli, ["info"])
        assert result.exit_code == 0
        assert "(no page loaded)" in result.output


class TestJSONOutput:
    """Test JSON output formatting."""

    def test_json_output_is_valid(self, runner):
        """JSON output should be valid and parseable."""
        result = runner.invoke(cli, ["--json", "status"])
        assert result.exit_code == 0
        import json
        data = json.loads(result.output)
        assert isinstance(data, dict)


class TestCleanup:
    """Cleanup tests to stop daemon if started."""

    def test_stop_daemon_if_running(self, runner):
        """Ensure daemon is stopped after tests."""
        result = runner.invoke(cli, ["daemon-stop"])
        # Should succeed whether daemon was running or not
        assert result.exit_code == 0

