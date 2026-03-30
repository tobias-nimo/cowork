import shutil
from pathlib import Path

from ..config import settings

_SRC = Path(__file__).resolve().parent.parent
_ROOT = Path(settings.project_root)

WORKSPACE = _ROOT / ".workspace"
SKILLS_SRC = _SRC / "skills"
SKILLS_DEST = WORKSPACE / "skills"
MEMORIES_DIR = WORKSPACE / "memories"
COWORK_MD = WORKSPACE / "COWORK.md"


def setup_workspace() -> None:
    """Initialise .workspace/ in the project root (idempotent).

    On first run this will:
    1. Create .workspace/
    2. Copy src/skills/ → .workspace/skills/
    3. Create an empty .workspace/memories/ directory
    4. Create an empty .workspace/COWORK.md file
    """
    if WORKSPACE.exists():
        return

    WORKSPACE.mkdir(parents=True)
    shutil.copytree(SKILLS_SRC, SKILLS_DEST)
    MEMORIES_DIR.mkdir()
    COWORK_MD.touch()
