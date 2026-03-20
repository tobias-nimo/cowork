# agent/graph.py

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from langchain_anthropic import ChatAnthropic
from pathlib import Path

from datetime import date

from ..config import settings
from ..prompts import prompts
from .subagents import subagents

from ..tools.mistral_ocr import to_md
from ..tools.md_convert import md_to_pdf, md_to_docx
from ..tools.view_image import view_image
from ..middleware import image_content_middleware
from ..utils import setup_workspace, SKILLS_DEST, AGENTS_MD

# --- Workspace ---
_ROOT = Path(settings.project_root)
setup_workspace()

# --- Chat Model ---
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=settings.anthropic_api_key)

# --- Backend ---
backend = LocalShellBackend(root_dir=settings.project_root, inherit_env=True)

# --- Deep Agent ---
cowork = create_deep_agent(
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
    skills=[str((SKILLS_DEST / "general").relative_to(_ROOT))],
    memory=[str(AGENTS_MD.relative_to(_ROOT))],

    # Tools
    tools=[to_md, md_to_pdf, md_to_docx, view_image], # + built-ins

    # HITL
    interrupt_on={
        "edit_file": True, # If True, default options are: approve, edit, reject
        "read_file": False,
        "write_file": False,
    },

    # Middleware
    middleware=[image_content_middleware],

    # Debug mode
     debug=settings.debug
)
