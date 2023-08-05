from pathlib import Path
from typing import Generator


from watchgraf.types import FileChange
from watchgraf._watchgrafrs import WatchGraf

def watch(path: Path) -> Generator[set[FileChange], None, None]:
    watcher = WatchGraf(str(path))
    while True:
        changes = watcher.watch()
        if changes:
            yield changes
