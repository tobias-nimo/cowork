"""
md_tools — outline & search tools for the local-research subagent.

Provides two LangChain tools:
  outline(file_path)  → heading hierarchy with line ranges
  search(query, ...)  → BM25-ranked section search with snippets
"""

from __future__ import annotations

import glob as _glob
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from langchain.tools import tool
from langchain_core.tools import ToolException
from rank_bm25 import BM25Okapi

from ..config import settings


# ──────────────────────────────────────────────
#  Data structures
# ──────────────────────────────────────────────


@dataclass
class HeadingNode:
    """A single heading in the document outline."""

    heading: str
    level: int
    line_start: int  # 1-indexed, inclusive
    line_end: int  # 1-indexed, inclusive
    children: list["HeadingNode"] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {
            "heading": self.heading,
            "level": self.level,
            "line_start": self.line_start,
            "line_end": self.line_end,
        }
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d


@dataclass
class Section:
    """A flat section extracted from the document (heading + body text)."""

    file: str
    heading: str
    level: int
    line_start: int
    line_end: int
    text: str


@dataclass
class SearchResult:
    """A single search hit."""

    file: str
    heading: str
    score: float
    line_start: int
    line_end: int
    snippet: str

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "heading": self.heading,
            "score": round(self.score, 4),
            "line_start": self.line_start,
            "line_end": self.line_end,
            "snippet": self.snippet,
        }


# ──────────────────────────────────────────────
#  Markdown parser — shared by both tools
# ──────────────────────────────────────────────

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")


def _parse_raw_headings(lines: list[str]) -> list[tuple[int, str, int]]:
    """Return [(level, text, line_number_1indexed), ...] for every md heading."""
    headings = []
    in_code_fence = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        m = _HEADING_RE.match(stripped)
        if m:
            headings.append((len(m.group(1)), m.group(2).strip(), i + 1))
    return headings


def _build_sections(file_path: str, lines: list[str]) -> list[Section]:
    """Split a markdown file into sections, one per heading."""
    headings = _parse_raw_headings(lines)
    total_lines = len(lines)
    sections: list[Section] = []

    first_heading_line = headings[0][2] if headings else total_lines + 1
    if first_heading_line > 1:
        preamble_text = "\n".join(lines[: first_heading_line - 1]).strip()
        if preamble_text:
            sections.append(
                Section(
                    file=file_path,
                    heading="(preamble)",
                    level=0,
                    line_start=1,
                    line_end=first_heading_line - 1,
                    text=preamble_text,
                )
            )

    for idx, (level, text, lnum) in enumerate(headings):
        if idx + 1 < len(headings):
            end = headings[idx + 1][2] - 1
        else:
            end = total_lines
        body = "\n".join(lines[lnum - 1 : end]).strip()
        sections.append(
            Section(
                file=file_path,
                heading=text,
                level=level,
                line_start=lnum,
                line_end=end,
                text=body,
            )
        )

    if not sections and lines:
        sections.append(
            Section(
                file=file_path,
                heading="(document)",
                level=0,
                line_start=1,
                line_end=total_lines,
                text="\n".join(lines).strip(),
            )
        )

    return sections


def _read_lines(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def _resolve_path(raw: str) -> Path:
    """Resolve a user-supplied path against project root."""
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path(settings.project_root) / path
    return path.resolve()


# ──────────────────────────────────────────────
#  TOOL 1: outline
# ──────────────────────────────────────────────


@tool
def outline(file_path: str) -> list[dict]:
    """Return the heading hierarchy of a markdown file with line ranges.

    Each entry contains heading text, level (1-6), line_start, line_end,
    and nested children. Use this to understand a document's structure
    before reading or searching specific sections.

    Args:
        file_path: Absolute or relative path to a markdown file.
    """
    try:
        path = _resolve_path(file_path)
        if not path.exists():
            raise ToolException(f"File not found: {path}")

        lines = _read_lines(str(path))
        headings = _parse_raw_headings(lines)
        total_lines = len(lines)

        if not headings:
            return [{"heading": "(document)", "level": 0, "line_start": 1, "line_end": total_lines}]

        flat: list[HeadingNode] = []
        for idx, (level, text, lnum) in enumerate(headings):
            if idx + 1 < len(headings):
                end = headings[idx + 1][2] - 1
            else:
                end = total_lines
            flat.append(HeadingNode(heading=text, level=level, line_start=lnum, line_end=end))

        root: list[HeadingNode] = []
        stack: list[HeadingNode] = []

        for node in flat:
            while stack and stack[-1].level >= node.level:
                stack.pop()
            if stack:
                stack[-1].children.append(node)
                stack[-1].line_end = max(stack[-1].line_end, node.line_end)
            else:
                root.append(node)
            stack.append(node)

        return [n.to_dict() for n in root]

    except ToolException:
        raise
    except Exception as e:
        raise ToolException(f"outline failed: {e}")


outline.handle_tool_error = True


# ──────────────────────────────────────────────
#  TOOL 2: search
# ──────────────────────────────────────────────


def _tokenize(text: str) -> list[str]:
    """Lowercase, split on non-alphanumeric, drop short tokens."""
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if len(t) > 1]


def _snippet(text: str, max_chars: int = 200) -> str:
    """First max_chars characters, cleaned up."""
    s = text.replace("\n", " ").strip()
    if len(s) <= max_chars:
        return s
    return s[:max_chars].rsplit(" ", 1)[0] + "…"


@tool
def search(
    query: str,
    file_path: Optional[str] = None,
    file_glob: Optional[str] = None,
    top_k: int = 5,
) -> list[dict]:
    """BM25-ranked semantic search across markdown sections.

    Splits markdown files into sections by heading, then ranks them
    against the query using BM25. Returns the most relevant sections
    with file path, heading, score, line range, and a text snippet.

    Provide either file_path (single file) or file_glob (e.g. "docs/**/*.md").

    Args:
        query: Natural language search query.
        file_path: Search a single markdown file.
        file_glob: Search multiple files by glob pattern (e.g. "docs/**/*.md").
                   Ignored if file_path is set.
        top_k: Max results to return (default 5).
    """
    try:
        # resolve files
        if file_path:
            resolved = _resolve_path(file_path)
            files = [str(resolved)]
        elif file_glob:
            base = str(Path(settings.project_root).resolve())
            pattern = file_glob if os.path.isabs(file_glob) else os.path.join(base, file_glob)
            files = sorted(_glob.glob(pattern, recursive=True))
        else:
            raise ToolException("Provide either file_path or file_glob")

        if not files:
            return []

        all_sections: list[Section] = []
        for fp in files:
            if not os.path.isfile(fp):
                continue
            lines = _read_lines(fp)
            all_sections.extend(_build_sections(fp, lines))

        if not all_sections:
            return []

        corpus_tokens = [_tokenize(s.text) for s in all_sections]
        query_tokens = _tokenize(query)

        if not query_tokens:
            return []

        bm25 = BM25Okapi(corpus_tokens)
        scores = bm25.get_scores(query_tokens)

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        results: list[dict] = []
        for idx, score in ranked[:top_k]:
            if score <= 0:
                break
            sec = all_sections[idx]
            results.append(
                SearchResult(
                    file=sec.file,
                    heading=sec.heading,
                    score=score,
                    line_start=sec.line_start,
                    line_end=sec.line_end,
                    snippet=_snippet(sec.text),
                ).to_dict()
            )

        return results

    except ToolException:
        raise
    except Exception as e:
        raise ToolException(f"search failed: {e}")


search.handle_tool_error = True
