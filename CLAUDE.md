# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A LangGraph-based multi-agent system ("cowork") built on LangChain Deep Agents. A coordinator agent orchestrates four specialized subagents (local research, web research, browser, Google Workspace) with an extensible skills system. Uses Claude Haiku 4.5 as the default LLM.

## Commands

```bash
# Install dependencies
uv sync

# Start LangGraph dev server (serves on http://localhost:2024)
uv run langgraph dev

# Run all tests
uv run pytest -v

# Run a single test
uv run pytest tests/test_config.py -v

# Lint
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
```

## Architecture

### Agent Graph

Entry point: `src/agents/deepagent.py` exports `cowork` (the LangGraph graph).

- **Main agent** (`deepagent.py`): Coordinator using `create_deep_agent()` with `LocalShellBackend`. Has tools for OCR (`to_md`), document conversion (`md_to_pdf`, `md_to_docx`), and image viewing (`view_image`). Uses HITL interrupts on `edit_file`.
- **local-research-subagent** (`subagents.py`): Local document search and analysis via BM25-ranked markdown section search (`outline`, `search`), OCR (`to_md`), and image viewing (`view_image`).
- **web-research-subagent** (`subagents.py`): Web search, extraction, crawling, and deep research via the Tavily CLI (`tvly`).
- **browser-subagent** (`subagents.py`): Browser automation (navigation, form filling, screenshots, data extraction) via the `browser-use` CLI.
- **gws-subagent** (`subagents.py`): Google Workspace operations (Drive, Gmail, Calendar, Docs, Sheets) via GWS MCP server.

### Skills System

Skills are markdown-based packages in `src/skills/<group>/<skill-name>/SKILL.md` with YAML frontmatter (name, description) and optional `scripts/`, `references/`, `assets/` directories. At runtime, skills are copied to `<project_root>/.workspace/skills/` by `src/utils/skills.py`. General skills load into the main agent; tavily skills into the research-subagent; browser skills into the browser-subagent; GWS skills into the gws-subagent.

### Prompts

System prompts are markdown files in `src/prompts/` loaded by `src/prompts/__init__.py` with variable injection (`{project_root}`, `{today_date}`). Files: `general.md` (main agent), `local-research.md`, `web-research.md`, `browser.md`, `gws.md`.

### Middleware

`src/middleware/image_content.py`: Intercepts `view_image` tool calls and rewrites ToolMessage with base64 multimodal image blocks.

### Configuration

`src/config.py` uses Pydantic Settings, loading from `.env`. Required: `ANTHROPIC_API_KEY`. Optional: `TAVILY_API_KEY`, `MISTRAL_API_KEY`, LangSmith keys, `PROJECT_ROOT`, `DEBUG`.

### Runtime Workspace

On first run, `src/utils/workspace.py:setup_workspace()` creates `.workspace/` in the project root containing:
- `skills/` — copied from `src/skills/`, loaded into agents at runtime
- `memories/` — empty dir for agent memory files (one markdown file per memory, with YAML frontmatter)
- `COWORK.md` — empty file for agent-managed notes
- `docs/` — created by OCR tool output

The workspace init is idempotent — skipped if `.workspace/` already exists.

## Key Conventions

- Python 3.12+, managed with `uv`
- Ruff for linting (line-length 100, ignores E501)
- pytest with `asyncio_mode = "auto"`
- LangGraph config in `langgraph.json` (graph ID: `cowork`)
- Node.js required for GWS MCP server
- Tavily CLI (`tvly`) required for research subagent
- `browser-use` CLI + `cloudflared` required for browser subagent
- Pandoc + XeLaTeX required for document conversion tools
