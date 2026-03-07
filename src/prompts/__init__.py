"""
Prompt loader — reads markdown files from this directory by name.

Usage::

    from src.prompts import prompts
    text = prompts.get("coordinator-agent")  # loads coordinator-agent.md
"""

from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent


class _Prompts:
    def get(self, name: str) -> str | None:
        path = _PROMPTS_DIR / f"{name}.md"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None


prompts = _Prompts()
