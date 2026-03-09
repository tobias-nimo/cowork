# LangChain + DeepAgents Development Guide

This project uses skills that contain up-to-date patterns and working reference scripts.

## CRITICAL: Invoke Skills BEFORE Writing Code

**ALWAYS** invoke the relevant skill first - skills have the correct imports, patterns, and scripts that prevent common mistakes.

### Getting Started
- **framework-selection** - Invoke when choosing between LangChain, LangGraph, and Deep Agents
- **langchain-dependencies** - Invoke before installing packages or when resolving version issues (Python + TypeScript)

### LangChain Skills
- **langchain-fundamentals** - Invoke for create_agent, @tool decorator, middleware patterns
- **langchain-rag** - Invoke for RAG pipelines, vector stores, embeddings
- **langchain-middleware** - Invoke for structured output with Pydantic

### LangGraph Skills
- **langgraph-fundamentals** - Invoke for StateGraph, state schemas, edges, Command, Send, invoke, streaming, error handling
- **langgraph-persistence** - Invoke for checkpointers, thread_id, time travel, memory, subgraph scoping
- **langgraph-human-in-the-loop** - Invoke for interrupts, human review, error handling, approval workflows

### DeepAgents Skills
- **deep-agents-core** - Invoke for DeepAgents harness architecture
- **deep-agents-memory** - Invoke for long-term memory with StoreBackend
- **deep-agents-orchestration** - Invoke for multi-agent coordination

## Project Structure

- **Main agent**: `src/agents/deepagent.py` — exports `cowork_agent`
- **Subagents**: `src/agents/subagents.py` — `research-subagent` (Tavily), `gws-subagent` (Google Workspace)
- **Tools**: `src/tools/` — `gws_mcp.py`, `tavily_mcp.py`, `groq.py`, `mistral_ocr.py`, `md_convert.py`
- **Skills**: `src/skills/general/` (main agent), `src/skills/gws/` (gws-subagent)
- **Prompts**: `src/prompts/` — `general.md`, `research.md`, `google.md`

## Environment Setup

Required environment variables:
```bash
GROQ_API_KEY=<your-key>      # LLM calls (all agents)
MISTRAL_API_KEY=<your-key>   # OCR via mistral_ocr.py
TAVILY_API_KEY=<your-key>    # Web search via tavily_mcp.py
```