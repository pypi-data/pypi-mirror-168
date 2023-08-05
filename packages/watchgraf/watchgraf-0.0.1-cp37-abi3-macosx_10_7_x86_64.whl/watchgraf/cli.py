import subprocess
from pathlib import Path
import shlex
import sys
import argparse
from typing import Literal, Optional, Union
from watchgraf.types import FileChange

from watchgraf.utils import ensure_it_is_command, resolve_path
from watchgraf.watcher import watch

def cli(*args_: str) -> None:
    args = args_ or sys.argv[1:]
    parser = argparse.ArgumentParser(prog="watchgraf")
    parser.add_argument('target', help='Command or dotted function path to run')
    parser.add_argument('paths', nargs='*', default='.', help='Paths to watch, defaults to current directory')

    arg_namespace = parser.parse_args(args)

    ensure_it_is_command(arg_namespace.target)

    paths = [resolve_path(path) for path in arg_namespace.paths]

    run_process(
        *paths,
        target=arg_namespace.target,
    )


def run_process(*paths: Path, target: str) -> int:
    process = start_process(target)
    process.wait()
    reloads = 0

    for _change in watch(*paths):
        process.terminate()
        process.wait()
        process = start_process(target)
        process.wait()

        reloads += 1
    
    process.terminate()
    process.wait()

    
    return reloads


def start_process(
    target: str,
    changes: Optional[set[FileChange]] = None,
) -> subprocess.Popen:
    #TODO: set the changes

    popen_args = shlex.split(target)
    process = subprocess.Popen(popen_args)
    return process
