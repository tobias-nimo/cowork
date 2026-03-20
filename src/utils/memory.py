import shutil
from pathlib import Path

from ..config import settings

_SRC = Path(__file__).resolve().parent.parent
_ROOT = Path(settings.project_root)

MEMORY_SRC = _SRC / "MEMORY.md"
MEMORY_DEST = _ROOT / ".workspace" / "memory"


def setup_memory() -> None:
    """Copy src/MEMORY.md to <project_root>/.workspace/memory/ if it doesn't already exist."""
    if not MEMORY_DEST.exists():
        MEMORY_DEST.mkdir(parents=True)
        shutil.copy2(MEMORY_SRC, MEMORY_DEST / MEMORY_SRC.name)


def memory_path() -> str:
    """Return the relative path to .workspace/memory/MEMORY.md."""
    setup_memory()
    return str((MEMORY_DEST / MEMORY_SRC.name).relative_to(_ROOT))
