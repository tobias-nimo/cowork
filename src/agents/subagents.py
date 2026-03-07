# agent/subagents.py

from langchain_groq import ChatGroq

from ..config import settings
from ..prompts import prompts
from ..tools.web_research import tavily_tools

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=settings.groq_api_key,
)

research_subagent = {
    "name": "research-subagent",
    "model": llm,
    "description": "Performs precise, in-depth web research and returns structured, reliable findings.",
    "system_prompt": prompts.get("research"),
    "tools": tavily_tools,
}

subagents = [research_subagent]