# DeepAgent Template

A production-ready template for building [**LangChain Deep Agents**](https://docs.langchain.com/oss/python/deepagents/overview) with [**Agent Chat UI**](https://github.com/langchain-ai/agent-chat-ui).

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | ≥ 3.12 | [python.org](https://python.org) |
| [uv](https://docs.astral.sh/uv/) | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Node.js | ≥ 18 | [nodejs.org](https://nodejs.org) |
| [gws](https://github.com/googleworkspace/cli) (Google Workspace CLI) | latest | `npm install -g @googleworkspace/cli` |

### Google Workspace auth (one-time)

```bash
gws auth setup   # creates GCP project and OAuth credentials
gws auth login   # authenticate with your Google account
```

## Quick Start

### 1. Clone and set up environment

```bash
git clone <repo-url>
cd deepagent-template

cp example.env .env
# Fill in your API keys in .env
```

### 2. Install backend dependencies

```bash
uv sync
```

### 3. Start the LangGraph backend

```bash
uv run langgraph dev
# Backend API: http://localhost:2024
# LangGraph Studio: https://smith.langchain.com/studio/?baseUrl=http://localhost:2024
```

### 4. Connect a chat UI

See the [Chat UI](#chat-ui) section below.

## Environment Variables

Copy `example.env` to `.env` and set the following:

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | [Groq](https://console.groq.com) API key (free tier available) |
| `TAVILY_API_KEY` | Yes | [Tavily](https://tavily.com) API key for web search |
| `LANGCHAIN_TRACING_V2` | No | Set to `true` to enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | No | LangSmith API key |
| `LANGCHAIN_PROJECT` | No | LangSmith project name |
| `PROJECT_ROOT` | No | Root directory for the filesystem backend (default: `.`) |

## Chat UI

This template ships **backend-only**. Connect any LangGraph-compatible chat UI to interact with the agent.

### Option A — Hosted Agent Chat UI (zero setup)

1. Open **[agentchat.vercel.app](https://agentchat.vercel.app)**
2. Enter your connection details:
   - **Deployment URL**: `http://localhost:2024` (local dev) or your deployed URL
   - **Graph ID**: `agent` (the key in `langgraph.json`)
   - **LangSmith API key**: optional, only needed for deployed (non-local) agents
3. Start chatting — the UI auto-detects tool calls and HITL interrupts.

### Option B — Run Agent Chat UI locally

```bash
git clone https://github.com/langchain-ai/agent-chat-ui.git
cd agent-chat-ui
pnpm install
pnpm dev
# Open: http://localhost:5173
```

Then enter the same connection details as above.

### Option C — LangGraph Studio

While `langgraph dev` is running, open LangGraph Studio at:

```
https://smith.langchain.com/studio/?baseUrl=http://localhost:2024
```

Studio lets you visually inspect graph runs, step through nodes, and replay traces.

---

## Project Structure

```
deepagent-template/
├── src/
│   ├── agent/
│   │   ├── graph.py          # Main LangGraph graph; exports `graph`
│   │   └── subagents.py      # Subagent definitions (research-agent)
│   ├── tools/
│   │   └── web_search_tools.py  # Tavily MCP tool loader
│   ├── prompts/
│   │   ├── __init__.py       # Prompt loader (reads .md files by name)
│   │   ├── coordinator-agent.md
│   │   └── research-subagent.md
│   ├── skills/
│   │   ├── skill-creator/    # Guidance for creating new skills
│   │   └── web-research/     # Structured web research workflow
│   ├── config.py             # Pydantic settings (loads from .env)
│   └── server.py             # Optional FastAPI server for custom endpoints
├── tests/                    # Pytest test suite
├── langgraph.json            # LangGraph server config
├── pyproject.toml            # Python dependencies and tooling
└── example.env               # Environment variable template
```

## LLM Configuration

The template defaults to **Groq** (free tier).

To switch providers, update `src/agent/graph.py` and `src/agent/subagents.py`:

```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", api_key=settings.openai_api_key)

# Anthropic
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-opus-4-6", api_key=settings.anthropic_api_key)
```

## Skills

Skills are markdown files that provide the agent with specialized knowledge and workflows.
They live in `src/skills/<skill-name>/SKILL.md`.

See `src/skills/skill-creator/SKILL.md` for the full guide.

## Human-in-the-Loop (HITL)

The coordinator agent pauses and waits for human approval before:
- Writing new files (`write_file`)
- Editing existing files (`edit_file`)

This is configured in `interrupt_on` inside `src/agent/graph.py`. Set a key to `False`
to disable interrupts for that tool.

## Running Tests

```bash
uv run pytest -v
```

## Development Tips

- **LangSmith Tracing**: set `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` to send
  traces to LangSmith for debugging.
- **Adding tools**: add LangChain tools to `src/tools/` and pass them to the appropriate
  subagent in `src/agent/subagents.py`.
