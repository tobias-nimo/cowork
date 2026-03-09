# agent/graph.py

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq

from ..config import settings
from ..prompts import prompts
from .subagents import subagents

from ..tools.md_convert import md_to_pdf, md_to_docx
from ..tools.groq import describe_image
from ..tools.mistral_ocr import to_md

# --- Chat Model ---
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=settings.groq_api_key,
)

# --- Backend ---
backend = LocalShellBackend(
    root_dir=settings.project_root,
    virtual_mode=True, # Only affects filesystem operations.
    inherit_env=False,
    )

# --- Deep Agent ---
cowork_agent = create_deep_agent(
    # LLM + system prompt
    model=llm,
    system_prompt=prompts.get("general"),

    # Core capabilities
    backend=backend,
    subagents=subagents,
    skills=["./src/skills/general/"],
    memory=["./src/AGENTS.md"],

    # Tools
    tools=[to_md, md_to_pdf, md_to_docx, describe_image], # + built-ins

    # HITL
    interrupt_on={
        "write_file": True,  # Default options: approve, edit, reject
        "edit_file": True,   # Default options: approve, edit, reject
        "read_file": False,
    },
    checkpointer=MemorySaver(), # Checkpointer is REQUIRED for human-in-the-loop!

     debug=settings.debug
)

