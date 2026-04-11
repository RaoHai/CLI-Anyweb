"""Shared REPL skin for cli-anyweb plugin scaffolds.

This plugin-level file intentionally mirrors the harness REPL utility so
site-specific CLIs can copy or import a consistent interface layer.
"""

from agent_harness.utils.repl_skin import ReplSkin

__all__ = ["ReplSkin"]

