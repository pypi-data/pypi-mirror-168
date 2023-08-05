from pathlib import Path
from time import sleep
from watchgraf.types import Change
from watchgraf.watcher import watch



def test_watch(tmp_path: Path, write_soon):
    sleep(0.05)
    write_soon(tmp_path / 'foo.txt')
    changes = None
    for changes in watch(tmp_path):
        break

    assert str(tmp_path / 'foo.txt') in changes

def test_watch_no_changes(tmp_path: Path, mocker):
    changes = []
    mocker.patch('watchgraf.watcher.WatchGraf.watch', side_effect=['new_change', None, 'value'])

    watch_generator = watch(tmp_path)
    change = next(watch_generator)
    changes.append(change)
    change = next(watch_generator)
    changes.append(change)

    assert len(changes) == 2
