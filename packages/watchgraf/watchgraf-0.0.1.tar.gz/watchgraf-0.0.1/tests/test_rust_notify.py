from pathlib import Path
import pytest

from watchgraf._watchgrafrs import WatchGraf

def test_add(temp_directory: Path):
    watcher = WatchGraf(str(temp_directory))
    (temp_directory / 'new_file.txt').write_text('hello')
    assert str(temp_directory / 'new_file.txt') in watcher.watch()