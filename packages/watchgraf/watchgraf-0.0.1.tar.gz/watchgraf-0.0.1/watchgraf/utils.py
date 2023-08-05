from pathlib import Path
import re
from typing import Literal


def ensure_it_is_command(target: str) -> bool:
    if '.' in target and not target.endswith(('.py', '.sh')):
        raise ValueError('target should be command only')
    return True

def resolve_path(path_str: str) -> Path:
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(path)
    return path.resolve()