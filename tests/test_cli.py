import sys

import pytest

from autopep723 import main


def test_cli_check_command(tmp_path, capsys):
    """Test CLI check command printing metadata to stdout."""
    script = tmp_path / "test_script.py"
    script.write_text("""import requests
import numpy as np
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "check", str(script)])
        main()

    captured = capsys.readouterr()
    assert "# /// script" in captured.out
    assert "requires-python" in captured.out


def test_cli_add_command(tmp_path):
    """Test CLI add command updating file with metadata."""
    script = tmp_path / "test_script.py"
    script.write_text("""import requests
print("Hello")
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "add", str(script)])
        main()

    # Check if file was updated
    updated_content = script.read_text()
    assert "# /// script" in updated_content
    assert '"requests"' in updated_content
    assert 'print("Hello")' in updated_content


def test_cli_custom_python_version(tmp_path, capsys):
    """Test CLI with custom Python version."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            sys,
            "argv",
            ["autopep723", "check", "--python-version", ">=3.11", str(script)],
        )
        main()

    captured = capsys.readouterr()
    assert 'requires-python = ">=3.11"' in captured.out


def test_cli_default_run_command(tmp_path, mocker):
    """Test CLI default run behavior."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=True)
    mock_run_with_uv = mocker.patch("autopep723.commands.run_with_uv")

    script = tmp_path / "test_script.py"
    script.write_text("""import requests
import numpy as np
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        main()

    # Verify run_with_uv was called with correct arguments
    mock_run_with_uv.assert_called_once()
    args = mock_run_with_uv.call_args[0]
    script_path, dependencies = args

    assert str(script_path) == str(script)
    assert "requests" in dependencies
    assert "numpy" in dependencies


def test_cli_nonexistent_file(mocker):
    """Test CLI with non-existent file."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=False)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "nonexistent.py"])
        with pytest.raises(SystemExit):
            main()


def test_cli_check_nonexistent_file():
    """Test CLI check command with non-existent file."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "check", "nonexistent.py"])
        with pytest.raises(SystemExit):
            main()


def test_cli_add_nonexistent_file():
    """Test CLI add command with non-existent file."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "add", "nonexistent.py"])
        with pytest.raises(SystemExit):
            main()


def test_cli_non_python_file_warning(tmp_path, mocker):
    """Test CLI with non-Python file shows warning."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=True)
    mocker.patch("autopep723.commands.run_with_uv")

    script = tmp_path / "test_script.txt"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        main()


def test_cli_run_with_dependencies_displays_info(tmp_path, mocker):
    """Test that CLI default run displays dependency information."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=True)
    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.return_value.returncode = 0

    script = tmp_path / "test_script.py"
    script.write_text("""import requests
import numpy as np
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        main()

    # Verify subprocess was called correctly
    expected_cmd = ["uv", "run", "--with", "numpy", "--with", "requests", str(script)]
    mock_subprocess.assert_called_once_with(expected_cmd, check=True)


def test_cli_run_no_dependencies(tmp_path, mocker):
    """Test CLI default run with script that has no dependencies."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=True)
    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.return_value.returncode = 0

    script = tmp_path / "test_script.py"
    script.write_text("""import os
import sys
print("Hello, world!")
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        main()

    # Should run uv without any --with flags
    expected_cmd = ["uv", "run", str(script)]
    mock_subprocess.assert_called_once_with(expected_cmd, check=True)


def test_cli_help_message(capsys):
    """Test CLI help message."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "--help"])
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "Auto-generate PEP 723 metadata" in captured.out
    assert "check" in captured.out
    assert "add" in captured.out
    assert "Examples:" in captured.out


def test_cli_version_message(capsys):
    """Test CLI version message."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "--version"])
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "1.0.0" in captured.out


def test_cli_add_with_existing_metadata(tmp_path):
    """Test CLI add command when file already has metadata."""
    script = tmp_path / "test_script.py"
    script.write_text("""#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["flask"]
# ///

import requests
import numpy as np
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "add", str(script)])
        main()

    # Check if file was updated correctly
    updated_content = script.read_text()
    assert "#!/usr/bin/env python3" in updated_content
    assert '"requests"' in updated_content
    assert '"numpy"' in updated_content
    assert '"flask"' not in updated_content  # Should be replaced
    assert 'requires-python = ">=3.13"' in updated_content  # Default version


def test_cli_syntax_error_file(tmp_path, capsys):
    """Test CLI check command with file containing syntax errors."""
    script = tmp_path / "test_script.py"
    script.write_text("""import requests
if True
    print("syntax error")
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "check", str(script)])
        main()

    captured = capsys.readouterr()
    # Should still generate metadata even with syntax errors
    assert "# /// script" in captured.out


def test_cli_empty_file(tmp_path, capsys):
    """Test CLI check command with empty Python file."""
    script = tmp_path / "test_script.py"
    script.write_text("")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "check", str(script)])
        main()

    captured = capsys.readouterr()
    assert "# /// script" in captured.out
    assert "dependencies" not in captured.out  # No dependencies section


def test_cli_run_with_existing_metadata(tmp_path, mocker):
    """Test CLI default run when script already has PEP 723 metadata."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=True)
    mocker.patch("autopep723.commands.has_pep723_metadata", return_value=True)
    mock_run_with_uv = mocker.patch("autopep723.commands.run_with_uv")

    script = tmp_path / "test_script.py"
    script.write_text("""# /// script
# requires-python = ">=3.13"
# dependencies = ["requests"]
# ///
import requests
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        main()

    # Should call run_with_uv with empty deps (let uv handle metadata)
    mock_run_with_uv.assert_called_once()
    args = mock_run_with_uv.call_args[0]
    script_path, dependencies = args
    assert str(script_path) == str(script)
    assert dependencies == []


def test_cli_uv_not_available(tmp_path, mocker):
    """Test CLI behavior when uv is not available."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=False)

    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        with pytest.raises(SystemExit):
            main()


def test_cli_no_arguments(capsys):
    """Test CLI with no arguments shows help."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723"])
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "usage:" in captured.out


def test_cli_check_with_python_version(tmp_path, capsys):
    """Test CLI check command with custom python version."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            sys,
            "argv",
            ["autopep723", "check", "--python-version", ">=3.12", str(script)],
        )
        main()

    captured = capsys.readouterr()
    assert 'requires-python = ">=3.12"' in captured.out


def test_cli_add_with_python_version(tmp_path):
    """Test CLI add command with custom python version."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            sys,
            "argv",
            ["autopep723", "add", "--python-version", ">=3.12", str(script)],
        )
        main()

    updated_content = script.read_text()
    assert 'requires-python = ">=3.12"' in updated_content


def test_cli_add_no_dependencies_message(tmp_path, caplog):
    """Test CLI add command shows message when no dependencies detected."""
    script = tmp_path / "test_script.py"
    script.write_text("""import os
import sys
print("Hello, world!")
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "add", str(script)])
        main()

    assert "No external dependencies found" in caplog.text


def test_cli_no_arguments_coverage():
    """Test CLI with only program name to cover is_default_run_command with no args."""
    from autopep723.cli import is_default_run_command

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723"])
        assert is_default_run_command() is False


def test_cli_add_remote_script_message(mocker, caplog):
    """Test CLI add command with remote script shows appropriate message."""
    # Mock is_url to return True
    mocker.patch("autopep723.validation.is_url", return_value=True)

    # Mock resolve_script_path to return a different path (simulating download)
    from pathlib import Path

    mock_temp_path = Path("/tmp/autopep723_test.py")
    mocker.patch("autopep723.commands.resolve_script_path", return_value=mock_temp_path)

    # Mock other functions
    mocker.patch("autopep723.commands.validate_script_input")
    mocker.patch("autopep723.commands.get_third_party_imports", return_value=["requests"])
    mocker.patch("autopep723.commands.generate_pep723_metadata", return_value="# metadata")
    mocker.patch("autopep723.commands.update_file_with_metadata")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "add", "https://example.com/script.py"])
        main()

    assert "Working with downloaded script at" in caplog.text
    assert "Cannot update original remote script." in caplog.text


def test_get_script_path_from_args_no_args():
    """Test get_script_path_from_args when no script path is provided (covers line 84)."""
    from autopep723.cli import get_script_path_from_args

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723"])
        with pytest.raises(ValueError, match="No script path provided"):
            get_script_path_from_args()


def test_logger_coverage(caplog, monkeypatch):
    """Quick test to cover missing logger lines."""

    from autopep723.logger import ColoredFormatter, init_logger, warning

    # Test NO_COLOR environment
    monkeypatch.setenv("NO_COLOR", "1")
    formatter = ColoredFormatter(use_colors=True)
    assert not formatter.use_colors

    # Test TERM=dumb
    monkeypatch.setenv("TERM", "dumb")
    formatter = ColoredFormatter(use_colors=True)
    assert not formatter.use_colors

    # Test warning function (line 79)
    warning("test warning message")
    assert "Warning: test warning message" in caplog.text

    # Test logger reinit
    init_logger(verbose=True, use_colors=False)
    init_logger(verbose=False, use_colors=False)


def test_main_with_verbose_flag(tmp_path, mocker):
    """Test main function with verbose flag to cover verbose reinitialization."""
    mocker.patch("autopep723.validation.check_uv_available", return_value=True)
    mock_init_logger = mocker.patch("autopep723.logger.init_logger")
    mocker.patch("autopep723.commands.run_with_uv")

    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "-v", str(script)])
        main()

    # Verify verbose logger was initialized
    mock_init_logger.assert_called_with(verbose=True)


def test_main_check_with_verbose(tmp_path, mocker, capsys):
    """Test main check command with verbose flag."""
    mock_init_logger = mocker.patch("autopep723.logger.init_logger")

    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "check", "--verbose", str(script)])
        main()

    # Verify verbose logger was initialized
    mock_init_logger.assert_called_with(verbose=True)


def test_main_add_with_verbose(tmp_path, mocker):
    """Test main add command with verbose flag."""
    mock_init_logger = mocker.patch("autopep723.logger.init_logger")

    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "add", "--verbose", str(script)])
        main()

    # Verify verbose logger was initialized
    mock_init_logger.assert_called_with(verbose=True)
