# agent/graph.py

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from langchain_groq import ChatGroq

from datetime import date

from ..config import settings
from ..prompts import prompts
from .subagents import subagents

from ..tools.md_convert import md_to_pdf, md_to_docx
from ..tools.groq import describe_image
from ..tools.mistral_ocr import to_md
from ..utils import skills_path, memory_path

# --- Chat Model ---
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=settings.groq_api_key,
)

# --- Backend ---
backend = LocalShellBackend(
    root_dir=settings.project_root,
    inherit_env=True,
    )

# --- Deep Agent ---
cowork_agent = create_deep_agent(
    # LLM + system prompt
    model=llm,
    system_prompt=prompts.get(
        "general",
        project_root=settings.project_root,
        today_date=str(date.today()),
    ),

    # Core capabilities
    backend=backend,
    subagents=subagents,
    skills=[skills_path("general")],
    memory=[memory_path()],

    # Tools
    tools=[to_md, md_to_pdf, md_to_docx, describe_image], # + execute + built-ins

    # HITL
    interrupt_on={
        "edit_file": False, # If True default options are: approve, edit, reject
        "read_file": False,
        "write_file": False,
    },

    # Debug mode
     debug=settings.debug
)

