# src/tools/md_convert.py

"""
Two tools to convert a local Markdown file into PDF or DOCX.
Both output files are saved next to the source .md file.

Requires: pandoc (https://pandoc.org/installing.html)

For PDF also requires a LaTeX engine → `apt install texlive-xetex` 
Or wkhtmltopdf → `apt install wkhtmltopdf`
"""

import subprocess
from pathlib import Path

from langchain.tools import tool
from langchain_core.tools import ToolException


# ── Helpers ───────────────────────────────────────────────────────────────────

def _resolve_md(md_path: str) -> Path:
    path = Path(md_path).expanduser().resolve()
    if not path.exists():
        raise ToolException(f"File not found: {path}")
    if path.suffix.lower() != ".md":
        raise ToolException(f"Expected a .md file, got: '{path.suffix}'")
    return path


def _run_pandoc(args: list[str]) -> None:
    """Run pandoc with the given args, raising ToolException on failure."""
    try:
        subprocess.run(
            ["pandoc", *args],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        raise ToolException(
            "pandoc is not installed or not on PATH. "
            "Install it with: brew install pandoc"
        )
    except subprocess.CalledProcessError as e:
        raise ToolException(f"pandoc failed:\n{e.stderr.strip()}")


# ── Tools ─────────────────────────────────────────────────────────────────────

@tool
def md_to_pdf(md_path: str) -> str:
    """
    Convert a local Markdown file to PDF.
    The PDF is saved next to the source file with the same name.
    Returns the absolute path to the generated PDF.
    """
    path = _resolve_md(md_path)
    output = path.with_suffix(".pdf")

    _run_pandoc([
        str(path),
        "-o", str(output),
        "--pdf-engine=xelatex", # swap for 'wkhtmltopdf' if no LaTeX installed
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
    ])

    return str(output)

@tool
def md_to_docx(md_path: str) -> str:
    """
    Convert a local Markdown file to DOCX.
    The DOCX is saved next to the source file with the same name.
    Returns the absolute path to the generated DOCX.
    """
    path = _resolve_md(md_path)
    output = path.with_suffix(".docx")

    _run_pandoc([
        str(path),
        "-o", str(output),
        "--from=markdown",
        "--to=docx",
    ])

    return str(output)

md_to_docx.handle_tool_error = True
md_to_pdf.handle_tool_error = True
