"""Tests for the Settings configuration module."""

from src.config import Settings


def test_settings_defaults():
    """Settings loads with empty strings for optional keys."""
    s = Settings()
    assert isinstance(s.groq_api_key, str)
    assert isinstance(s.tavily_api_key, str)
    assert isinstance(s.openai_api_key, str)
    assert isinstance(s.anthropic_api_key, str)


def test_settings_server_defaults():
    """Server defaults are correct."""
    s = Settings()
    assert s.host == "0.0.0.0"
    assert s.port == 8000


def test_settings_project_root_default():
    """Project root defaults to current directory."""
    s = Settings()
    assert s.project_root == "."


def test_settings_tracing_default():
    """LangSmith tracing is disabled by default."""
    s = Settings()
    assert s.langchain_tracing_v2 is False


def test_settings_override(monkeypatch):
    """Environment variables override defaults."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key-123")
    monkeypatch.setenv("PORT", "9000")
    s = Settings()
    assert s.groq_api_key == "test-key-123"
    assert s.port == 9000
