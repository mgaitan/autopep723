"""Tests for validation module."""

import subprocess

import pytest

from autopep723.validation import (
    check_script_extension,
    check_uv_available,
    validate_and_prepare_script,
    validate_script_exists,
    validate_uv_available,
)


def test_validate_script_exists_success(tmp_path):
    """Test validate_script_exists with existing file."""
    script = tmp_path / "test_script.py"
    script.write_text("print('hello')")

    result = validate_script_exists(script)
    assert result is True


def test_validate_script_exists_failure(tmp_path):
    """Test validate_script_exists with non-existent file."""
    script = tmp_path / "nonexistent.py"

    with pytest.raises(SystemExit):
        validate_script_exists(script)


def test_check_script_extension_py_file(tmp_path, capsys):
    """Test check_script_extension with .py file (no warning)."""
    script = tmp_path / "test_script.py"
    script.write_text("print('hello')")

    check_script_extension(script)

    captured = capsys.readouterr()
    assert captured.out == ""


def test_check_script_extension_non_py_file(tmp_path, capsys):
    """Test check_script_extension with non-.py file (shows warning)."""
    script = tmp_path / "test_script.txt"
    script.write_text("print('hello')")

    check_script_extension(script)

    captured = capsys.readouterr()
    assert "does not have a .py extension" in captured.out


def test_check_uv_available_true(mocker):
    """Test check_uv_available when uv is available."""
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value.returncode = 0

    result = check_uv_available()
    assert result is True
    mock_subprocess.assert_called_once_with(["uv", "--version"], capture_output=True, check=True)


def test_check_uv_available_false_not_found(mocker):
    """Test check_uv_available when uv is not found."""
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.side_effect = FileNotFoundError()

    result = check_uv_available()
    assert result is False


def test_check_uv_available_false_error(mocker):
    """Test check_uv_available when uv returns error."""
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.side_effect = subprocess.CalledProcessError(1, "uv")

    result = check_uv_available()
    assert result is False


def test_validate_uv_available_success(mocker):
    """Test validate_uv_available when uv is available."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=True)

    result = validate_uv_available()
    assert result is True


def test_validate_uv_available_failure(mocker):
    """Test validate_uv_available when uv is not available."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=False)

    with pytest.raises(SystemExit):
        validate_uv_available()


def test_validate_and_prepare_script_success(tmp_path, mocker):
    """Test validate_and_prepare_script with valid .py file."""
    script = tmp_path / "test_script.py"
    script.write_text("print('hello')")

    # Should not raise any exceptions
    validate_and_prepare_script(script)


def test_validate_and_prepare_script_non_py_warning(tmp_path, capsys):
    """Test validate_and_prepare_script with non-.py file shows warning."""
    script = tmp_path / "test_script.txt"
    script.write_text("print('hello')")

    validate_and_prepare_script(script)

    captured = capsys.readouterr()
    assert "does not have a .py extension" in captured.out


def test_validate_and_prepare_script_nonexistent(tmp_path):
    """Test validate_and_prepare_script with non-existent file."""
    script = tmp_path / "nonexistent.py"

    with pytest.raises(SystemExit):
        validate_and_prepare_script(script)


@pytest.mark.parametrize(
    "extension,should_warn",
    [
        (".py", False),
        (".txt", True),
    ],
)
def test_check_script_extension_parametrized(tmp_path, capsys, extension, should_warn):
    """Test check_script_extension with various extensions."""
    script = tmp_path / f"test_script{extension}"
    script.write_text("print('hello')")

    check_script_extension(script)

    captured = capsys.readouterr()
    if should_warn:
        assert "does not have a .py extension" in captured.out
    else:
        assert captured.out == ""


def test_validate_uv_available_error_messages(mocker, capsys):
    """Test validate_uv_available error messages."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=False)

    with pytest.raises(SystemExit):
        validate_uv_available()

    captured = capsys.readouterr()
    assert "'uv' is not installed or not available in PATH" in captured.err
    assert "Please install uv: https://github.com/astral-sh/uv" in captured.err


def test_validate_script_exists_error_message(tmp_path, capsys):
    """Test validate_script_exists error message."""
    script = tmp_path / "nonexistent.py"

    with pytest.raises(SystemExit):
        validate_script_exists(script)

    captured = capsys.readouterr()
    assert "does not exist" in captured.err
