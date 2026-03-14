# agent/subagents.py

from langchain_groq import ChatGroq

from ..config import settings
from ..prompts import prompts

from ..tools.tavily_mcp import web_search_tools

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=settings.groq_api_key,
)

research_subagent = {
    "name": "research-subagent",
    "model": llm,
    "description": "Performs precise, in-depth web research and returns structured, reliable findings.",
    "system_prompt": prompts.get("research"),
    "tools": web_search_tools,
}

gws_subagent = {
    "name": "gws-subagent",
    "model": llm,
    "description": " Interacts with the full Google Workspace suite (Drive, Gmail, Calendar, Docs and Sheets) via the gws MCP — use it to read/write files in drive, manage emails, schedule events.",
    "system_prompt": prompts.get("google"),
    "skills": ["./src/skills/gws/"],
}

subagents = [research_subagent, gws_subagent]