from pathlib import Path


def gather_skills(directory: str) -> list[str]:
    """Return a list of paths for each skill (subdirectory) in the given directory."""
    return [str(p) for p in sorted(Path(directory).iterdir()) if p.is_dir()]
