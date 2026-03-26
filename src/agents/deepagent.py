# agent/graph.py

from pathlib import Path
from datetime import date

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from langchain_anthropic import ChatAnthropic

from ..config import settings
from ..prompts import prompts
from .subagents import subagents

from ..tools.mistral_ocr import to_md
from ..tools.view_image import view_image
from ..middleware import image_content_middleware
from ..utils import setup_workspace, SKILLS_DEST, AGENTS_MD

# Set up .workspace/
_ROOT = Path(settings.project_root)
setup_workspace()

# Deep Agent
cowork = create_deep_agent(
    # LLM
    model=ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=settings.anthropic_api_key
    ),
    
    # System prompt
    system_prompt=prompts.get(
        "general",
        project_root=settings.project_root,
        today_date=str(date.today()),
    ),

    # SubAgents
    subagents=subagents,

    # Skills + Memory
    skills=[str((SKILLS_DEST / "general").relative_to(_ROOT))],
    memory=[str(AGENTS_MD.relative_to(_ROOT))],

    # Tools
    tools=[
        to_md,
        view_image
    ], # + built-ins

    # HITL
    interrupt_on={
        "edit_file": True, # If True, default options are: approve, edit, reject
        "read_file": False,
        "write_file": False,
    },

    # Backend
    backend=LocalShellBackend(
        root_dir=settings.project_root,
        inherit_env=True
    ), # adds exec tool

    # Middleware
    middleware=[image_content_middleware],

    # Debug mode
     debug=settings.debug
)
