# agent/graph.py

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
#from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq

from ..config import settings
from ..prompts import prompts
from .subagents import subagents

# --- Chat Model ---
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=settings.groq_api_key,
)

# --- Backend ---
backend = FilesystemBackend(root_dir=settings.project_root, virtual_mode=True)

# --- Deep Agent ---
deepagent = create_deep_agent(
    # LLM + system prompt
    model=llm,
    system_prompt=prompts.get("general"),

    # Core capabilities
    backend=backend,
    subagents=subagents,
    skills=["./src/skills/"],
    memory=["./src/AGENTS.md"],

    # Tools
    tools=[],

    # HITL
    interrupt_on={
        "write_file": True,  # Default: approve, edit, reject
        "read_file": False,  # No interrupts needed
        "edit_file": True,   # Default: approve, edit, reject
    },
    #checkpointer=InMemorySaver(), # Checkpointer is REQUIRED for human-in-the-loop!
    # But LangGraph API platform manages persistence - No checkpointer needed.

     debug=settings.debug
)

