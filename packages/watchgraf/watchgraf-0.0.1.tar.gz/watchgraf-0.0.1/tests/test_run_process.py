from unittest.mock import MagicMock
from watchgraf.cli import run_process, start_process

import pytest
from pytest_mock.plugin import MockerFixture

def test_alive_terminates(mocker: MockerFixture):
    m = MagicMock()
    popen_mock = mocker.patch('watchgraf.cli.subprocess.Popen', return_value=m)
    mocker.patch('watchgraf.cli.watch', return_value=['test'])
    
    assert run_process('/x/y/z', target='ls') == 1
    popen_mock.assert_called_with(['ls'])
    assert popen_mock.call_count == 2
    assert m.terminate.call_count == 2
    assert m.wait.call_count == 4 # ensure that process is started everytime


def test_start_process(mocker: MockerFixture):
    m = MagicMock()
    process_mock = mocker.patch('watchgraf.cli.subprocess.Popen', return_value=m)
    process = start_process('ls')
    assert m == process
    process_mock.assert_called_with(['ls'])
