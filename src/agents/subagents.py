# agent/subagents.py

from pathlib import Path

#from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq

from ..config import settings
from ..prompts import prompts
from ..utils import SKILLS_DEST

from ..tools.md_tools import outline, search
from ..tools.mistral_ocr import to_md
from ..tools.view_image import view_image


_ROOT = Path(settings.project_root)

#llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=settings.anthropic_api_key)
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=settings.groq_api_key)

web_research_subagent = {
    "name": "web-research-subagent",
    "model": llm,
    "description": "Performs precise, in-depth web research and returns structured, reliable findings.",
    "system_prompt": prompts.get("web-research"),
    "skills": [str((SKILLS_DEST / "tavily").relative_to(_ROOT))]
}

local_research_subagent = {
    "name": "local-research-subagent",
    "model": llm,
    "description": "Searches, navigates, and analyzes local documents and files — use it to find information in large markdown files within the workspace.",
    "system_prompt": prompts.get("local-research"),
    "tools": [to_md, outline, search, view_image]
}

gws_subagent = {
    "name": "gws-subagent",
    "model": llm,
    "description": "Interacts with the full Google Workspace suite (Drive, Gmail, Calendar, Docs and Sheets) via the gws MCP — use it to read/write files in drive, manage emails, schedule events.",
    "system_prompt": prompts.get("google"),
    "skills": [str((SKILLS_DEST / "gws").relative_to(_ROOT))],
}

browser_subagent = {
    "name": "browser-subagent",
    "model": llm,
    "description": "Automates browser interactions — navigates websites, fills forms, extracts data, takes screenshots, and handles authenticated sessions via the browser-use CLI.",
    "system_prompt": prompts.get("browser"),
    "skills": [str((SKILLS_DEST / "browser").relative_to(_ROOT))],
}

subagents = [
    local_research_subagent,
    web_research_subagent,
    browser_subagent,
    gws_subagent
]