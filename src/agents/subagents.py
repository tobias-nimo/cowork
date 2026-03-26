# agent/subagents.py

from pathlib import Path

from langchain_anthropic import ChatAnthropic

from ..config import settings
from ..prompts import prompts
from ..utils import SKILLS_DEST

_ROOT = Path(settings.project_root)

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=settings.anthropic_api_key)

research_subagent = {
    "name": "research-subagent",
    "model": llm,
    "description": "Performs precise, in-depth web research and returns structured, reliable findings.",
    "system_prompt": prompts.get("research"),
    "skills": [str((SKILLS_DEST / "tavily").relative_to(_ROOT))]
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

subagents = [research_subagent, browser_subagent, gws_subagent]