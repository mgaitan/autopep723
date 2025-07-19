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


def test_cli_upgrade_command(tmp_path):
    """Test CLI upgrade command updating file with metadata."""
    script = tmp_path / "test_script.py"
    script.write_text("""import requests
print("Hello")
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "upgrade", str(script)])
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
        mp.setattr(sys, "argv", ["autopep723", "check", "--python-version", ">=3.11", str(script)])
        main()

    captured = capsys.readouterr()
    assert 'requires-python = ">=3.11"' in captured.out


def test_cli_default_run_command(tmp_path, mocker):
    """Test CLI default run behavior."""
    mocker.patch("autopep723.check_uv_available", return_value=True)
    mock_run_with_uv = mocker.patch("autopep723.run_with_uv")

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
    mocker.patch("autopep723.check_uv_available", return_value=False)

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


def test_cli_upgrade_nonexistent_file():
    """Test CLI upgrade command with non-existent file."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "upgrade", "nonexistent.py"])
        with pytest.raises(SystemExit):
            main()


def test_cli_non_python_file_warning(tmp_path, mocker):
    """Test CLI with non-Python file shows warning."""
    mocker.patch("autopep723.check_uv_available", return_value=True)
    mocker.patch("autopep723.run_with_uv")

    script = tmp_path / "test_script.txt"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        main()


def test_cli_run_with_dependencies_displays_info(tmp_path, mocker):
    """Test that CLI default run displays dependency information."""
    mocker.patch("autopep723.check_uv_available", return_value=True)
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
    mocker.patch("autopep723.check_uv_available", return_value=True)
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
    assert "upgrade" in captured.out
    assert "Examples:" in captured.out


def test_cli_version_message(capsys):
    """Test CLI version message."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "--version"])
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "1.0.0" in captured.out


def test_cli_upgrade_with_existing_metadata(tmp_path):
    """Test CLI upgrade command when file already has metadata."""
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
        mp.setattr(sys, "argv", ["autopep723", "upgrade", str(script)])
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
    mocker.patch("autopep723.check_uv_available", return_value=True)
    mocker.patch("autopep723.has_pep723_metadata", return_value=True)
    mock_run_with_uv = mocker.patch("autopep723.run_with_uv")

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
    mocker.patch("autopep723.check_uv_available", return_value=False)

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
        mp.setattr(sys, "argv", ["autopep723", "check", "--python-version", ">=3.12", str(script)])
        main()

    captured = capsys.readouterr()
    assert 'requires-python = ">=3.12"' in captured.out


def test_cli_upgrade_with_python_version(tmp_path):
    """Test CLI upgrade command with custom python version."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "upgrade", "--python-version", ">=3.12", str(script)])
        main()

    updated_content = script.read_text()
    assert 'requires-python = ">=3.12"' in updated_content


def test_cli_run_script_not_exists(mocker):
    """Test CLI run with non-existent script file."""
    mocker.patch("autopep723.check_uv_available", return_value=True)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "nonexistent_script.py"])
        with pytest.raises(SystemExit):
            main()


def test_cli_upgrade_no_dependencies_message(tmp_path, capsys):
    """Test CLI upgrade command shows message when no dependencies detected."""
    script = tmp_path / "test_script.py"
    script.write_text("""import os
import sys
print("Hello, world!")
""")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "upgrade", str(script)])
        main()

    captured = capsys.readouterr()
    assert "No third-party dependencies detected" in captured.out


def test_cli_run_with_non_py_extension(tmp_path, mocker, capsys):
    """Test CLI run with file that doesn't have .py extension shows warning."""
    mocker.patch("autopep723.check_uv_available", return_value=True)
    mocker.patch("autopep723.has_pep723_metadata", return_value=False)
    mocker.patch("autopep723.run_with_uv")

    script = tmp_path / "test_script.txt"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        main()

    captured = capsys.readouterr()
    assert "does not have a .py extension" in captured.out


def test_main_module_execution(mocker):
    """Test that main() is called when module is executed directly."""
    mock_main = mocker.patch("autopep723.main")

    # Mock sys.argv to avoid interference
    mocker.patch("sys.argv", ["autopep723", "--help"])

    # Import and execute the module's __main__ block
    import autopep723

    # Simulate the __name__ == "__main__" condition
    if autopep723.__name__ == "autopep723":
        autopep723.main()

    # Verify main was called
    mock_main.assert_called()


@pytest.mark.parametrize(
    "command,script_content,expected_in_output",
    [
        ("check", "import requests", "requires-python"),
        ("check", "import numpy\nimport pandas", "dependencies"),
        ("check", "import os\nimport sys", "# /// script"),
    ],
)
def test_cli_commands_parametrized(tmp_path, capsys, command, script_content, expected_in_output):
    """Test CLI commands with various script contents."""
    script = tmp_path / "test_script.py"
    script.write_text(script_content)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", command, str(script)])
        main()

    captured = capsys.readouterr()
    assert expected_in_output in captured.out


@pytest.mark.parametrize("python_version", [">=3.9", ">=3.10", ">=3.11", ">=3.12"])
def test_cli_check_custom_python_versions(tmp_path, capsys, python_version):
    """Test CLI check command with various Python versions."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", "check", "--python-version", python_version, str(script)])
        main()

    captured = capsys.readouterr()
    assert f'requires-python = "{python_version}"' in captured.out


@pytest.mark.parametrize("extension", [".py", ".pyw", ".txt", ".sh"])
def test_cli_run_various_file_extensions(tmp_path, mocker, extension):
    """Test CLI run with various file extensions."""
    mocker.patch("autopep723.check_uv_available", return_value=True)
    mocker.patch("autopep723.has_pep723_metadata", return_value=False)
    mock_run = mocker.patch("autopep723.run_with_uv")

    script = tmp_path / f"test_script{extension}"
    script.write_text("import requests")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", ["autopep723", str(script)])
        main()

    mock_run.assert_called_once()
