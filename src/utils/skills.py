import shutil
from pathlib import Path

from ..config import settings

_SRC = Path(__file__).resolve().parent.parent
_ROOT = Path(settings.project_root)

SKILLS_SRC = _SRC / "skills"
SKILLS_DEST = _ROOT / ".skills"


def setup_skills() -> None:
    """Copy src/skills/ to <project_root>/.skills/ if it doesn't already exist."""
    if not SKILLS_DEST.exists():
        shutil.copytree(SKILLS_SRC, SKILLS_DEST)


def skills_path(group: str) -> str:
    """Return the relative path to .skills/<group>/."""
    setup_skills()
    return str((SKILLS_DEST / group).relative_to(_ROOT))
