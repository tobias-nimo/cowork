"""Tests for the prompts loader module."""

from src.prompts import prompts


def test_load_existing_prompt():
    """Returns the content of an existing markdown prompt file."""
    content = prompts.get("coordinator-agent")
    assert content is not None
    assert len(content) > 0
    assert isinstance(content, str)


def test_load_research_subagent_prompt():
    """research-subagent.md can be loaded."""
    content = prompts.get("research-subagent")
    assert content is not None
    assert len(content) > 0


def test_missing_prompt_returns_none():
    """Returns None for a prompt file that does not exist."""
    result = prompts.get("nonexistent-prompt-xyz")
    assert result is None


def test_prompt_content_coordinator():
    """Coordinator agent prompt contains expected keywords."""
    content = prompts.get("coordinator-agent")
    assert content is not None
    assert "coordinator" in content.lower() or "plan" in content.lower()


def test_prompt_content_research():
    """Research subagent prompt contains expected keywords."""
    content = prompts.get("research-subagent")
    assert content is not None
    assert "research" in content.lower() or "search" in content.lower()
