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

from ..config import settings


# ── Helpers ───────────────────────────────────────────────────────────────────

def _resolve_md(md_path: str) -> Path:
    path = Path(md_path).expanduser()
    if not path.is_absolute():
        path = Path(settings.project_root) / path
    path = path.resolve()
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

def _resolve_output(output_path: str, suffix: str) -> Path:
    path = Path(output_path).expanduser()
    if not path.is_absolute():
        path = Path(settings.project_root) / path
    path = path.resolve()
    if path.suffix.lower() != suffix:
        path = path.with_suffix(suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@tool
def md_to_pdf(md_path: str, output_path: str) -> str:
    """
    Convert a local Markdown file to PDF.
    Returns the absolute path to the generated PDF.

    Args:
        md_path: Path to the source .md file.
        output_path: Path where the PDF will be saved.
    """
    path = _resolve_md(md_path)
    output = _resolve_output(output_path, ".pdf")

    _run_pandoc([
        str(path),
        "-o", str(output),
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
    ])

    return str(output)

@tool
def md_to_docx(md_path: str, output_path: str) -> str:
    """
    Convert a local Markdown file to DOCX.
    Returns the absolute path to the generated DOCX.

    Args:
        md_path: Path to the source .md file.
        output_path: Path where the DOCX will be saved.
    """
    path = _resolve_md(md_path)
    output = _resolve_output(output_path, ".docx")

    _run_pandoc([
        str(path),
        "-o", str(output),
        "--from=markdown",
        "--to=docx",
    ])

    return str(output)

md_to_docx.handle_tool_error = True
md_to_pdf.handle_tool_error = True
