"""
Structural tests for graph-adjacent modules.

Importing src.agent.graph (or src.tools.web_search_tools) requires a running
Tavily MCP server and valid API keys.  These tests cover only the modules that
can be exercised without external services.
"""


def test_prompts_module_structure():
    """The _Prompts class exposes a callable .get() method."""
    from src.prompts import _Prompts, prompts

    assert hasattr(prompts, "get")
    assert callable(prompts.get)
    assert isinstance(prompts, _Prompts)


def test_config_module_importable():
    """Config module imports cleanly and settings is the right type."""
    from src.config import Settings, settings

    assert settings is not None
    assert isinstance(settings, Settings)


def test_all_prompt_files_load():
    """Both expected prompt files are readable and non-empty."""
    from src.prompts import prompts

    for name in ("coordinator-agent", "research-subagent"):
        content = prompts.get(name)
        assert content is not None, f"Prompt '{name}' not found"
        assert len(content.strip()) > 0, f"Prompt '{name}' is empty"


def test_settings_fields_present():
    """All expected API-key fields exist on Settings."""
    from src.config import Settings

    fields = Settings.model_fields
    for field in ("groq_api_key", "tavily_api_key", "openai_api_key", "anthropic_api_key"):
        assert field in fields, f"Missing field: {field}"
