from pathlib import Path
from threading import Thread
import pytest
from time import sleep

def sleep_write(path: Path):
    sleep(0.1)
    path.write_text('hello')

@pytest.fixture
def temp_directory(tmp_path):
    tmp_directory: Path = tmp_path / "tmp_dir"
    tmp_directory.mkdir()
    yield tmp_directory

    for file in tmp_directory.iterdir():
        file.unlink()
    
    tmp_directory.rmdir()


@pytest.fixture
def write_soon():
    threads: list[Thread] = []

    def start(path: Path):
        thread = Thread(target=sleep_write, args=(path,))
        thread.start()
        threads.append(thread)
    
    yield start

    [t.join() for t in threads]
