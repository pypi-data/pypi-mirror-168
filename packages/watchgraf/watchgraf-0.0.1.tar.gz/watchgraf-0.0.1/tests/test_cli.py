import pytest
from pytest_mock.plugin import MockerFixture
from watchgraf.cli import cli

def test_cli_function(mocker: MockerFixture, tmp_path):

    mock_run_process = mocker.patch('watchgraf.cli.run_process')
    cli('ls', str(tmp_path))
    mock_run_process.assert_called_once_with(
        tmp_path,
        target='ls',
    )

def test_cli_function_path_not_exist(mocker: MockerFixture):
    with pytest.raises(FileNotFoundError):
        cli('ls', 'path_dont_exist')

def test_cli_function_function_argument_not_implemented(mocker: MockerFixture, tmp_path):
    with pytest.raises(ValueError):
        cli('os.sys', str(tmp_path))