from pathlib import Path

import pytest

from autopep723 import (
    IMPORT_TO_PACKAGE_MAP,
    check_uv_available,
    download_script,
    extract_existing_metadata,
    generate_pep723_metadata,
    get_builtin_modules,
    get_third_party_imports,
    has_existing_metadata,
    has_pep723_metadata,
    is_url,
    resolve_script_path,
    run_with_uv,
    update_file_with_metadata,
)


def test_get_builtin_modules_returns_set():
    """Test that get_builtin_modules returns a set."""
    modules = get_builtin_modules()
    assert isinstance(modules, set)
    assert len(modules) > 0


def test_get_builtin_modules_includes_common_modules():
    """Test that common modules are included in builtin modules."""
    modules = get_builtin_modules()
    assert "sys" in modules
    assert "os" in modules


def test_simple_import(tmp_path):
    """Test detection of simple third-party imports."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests\nimport os\n")

    imports = get_third_party_imports(script)
    assert "requests" in imports
    assert "os" not in imports


def test_from_import(tmp_path):
    """Test detection of from imports."""
    script = tmp_path / "test_script.py"
    script.write_text("from bs4 import BeautifulSoup\nfrom os import path\n")

    imports = get_third_party_imports(script)
    assert "beautifulsoup4" in imports  # Should be mapped
    assert "os" not in imports


def test_import_mapping(tmp_path):
    """Test that import names are correctly mapped to package names."""
    script = tmp_path / "test_script.py"
    script.write_text("import PIL\nimport cv2\nimport sklearn\n")

    imports = get_third_party_imports(script)
    assert "Pillow" in imports
    assert "opencv-python" in imports
    assert "scikit-learn" in imports
    assert "PIL" not in imports
    assert "cv2" not in imports
    assert "sklearn" not in imports


def test_complex_imports(tmp_path):
    """Test complex import scenarios."""
    code = """
import requests
from flask import Flask, render_template
import numpy as np
from sklearn.model_selection import train_test_split
import os
import sys
from pathlib import Path
"""
    script = tmp_path / "test_script.py"
    script.write_text(code)

    imports = get_third_party_imports(script)
    expected = ["flask", "numpy", "requests", "scikit-learn"]
    for pkg in expected:
        assert pkg in imports

    # Built-in modules should not be included
    builtin_should_not_be_present = ["os", "sys", "pathlib"]
    for pkg in builtin_should_not_be_present:
        assert pkg not in imports


def test_syntax_error_handling(tmp_path):
    """Test handling of files with syntax errors."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests\nif True\n  print('syntax error')")

    imports = get_third_party_imports(script)
    assert imports == []  # Should return empty list on syntax error


def test_empty_file(tmp_path):
    """Test handling of empty files."""
    script = tmp_path / "test_script.py"
    script.write_text("")

    imports = get_third_party_imports(script)
    assert imports == []


def test_generate_metadata_no_dependencies():
    """Test metadata generation with no dependencies."""
    metadata = generate_pep723_metadata([])
    expected = """# /// script
# requires-python = ">=3.13"
# ///"""
    assert metadata == expected


def test_generate_metadata_with_dependencies():
    """Test metadata generation with dependencies."""
    deps = ["requests", "flask", "numpy"]
    metadata = generate_pep723_metadata(deps)

    assert "# /// script" in metadata
    assert "# ///" in metadata
    assert 'requires-python = ">=3.13"' in metadata
    assert "dependencies = [" in metadata
    assert '"requests"' in metadata
    assert '"flask"' in metadata
    assert '"numpy"' in metadata


def test_generate_metadata_custom_python_version():
    """Test metadata generation with custom Python version."""
    deps = ["requests"]
    metadata = generate_pep723_metadata(deps, ">=3.11")
    assert 'requires-python = ">=3.11"' in metadata


def test_generate_metadata_single_dependency():
    """Test metadata generation with single dependency."""
    deps = ["requests"]
    metadata = generate_pep723_metadata(deps)
    expected = """# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///"""
    assert metadata == expected


def test_has_existing_metadata_true():
    """Test detection of existing metadata."""
    content = """#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["requests"]
# ///

import requests
"""
    assert has_existing_metadata(content) is True


def test_has_existing_metadata_false():
    """Test detection when no metadata exists."""
    content = """#!/usr/bin/env python3
import requests
"""
    assert has_existing_metadata(content) is False


def test_extract_existing_metadata():
    """Test extraction of existing metadata."""
    content = """#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["requests"]
# ///

import requests
print("Hello")
"""
    before, metadata, after = extract_existing_metadata(content)

    assert before == "#!/usr/bin/env python3\n"
    assert "# /// script" in metadata
    assert "# ///" in metadata
    assert after == '\nimport requests\nprint("Hello")\n'


def test_extract_no_existing_metadata():
    """Test extraction when no metadata exists."""
    content = "import requests\nprint('hello')"
    before, metadata, after = extract_existing_metadata(content)

    assert before == content
    assert metadata == ""
    assert after == ""


def test_update_file_new_metadata(tmp_path):
    """Test updating file with new metadata."""
    script = tmp_path / "test_script.py"
    original_content = """import requests
print("Hello")
"""
    script.write_text(original_content)

    metadata = """# /// script
# requires-python = ">=3.13"
# dependencies = ["requests"]
# ///"""

    update_file_with_metadata(script, metadata)

    updated_content = script.read_text()
    assert "# /// script" in updated_content
    assert "import requests" in updated_content
    assert 'print("Hello")' in updated_content


def test_update_file_with_shebang(tmp_path):
    """Test updating file that has shebang."""
    script = tmp_path / "test_script.py"
    original_content = """#!/usr/bin/env python3
import requests
print("Hello")
"""
    script.write_text(original_content)

    metadata = """# /// script
# requires-python = ">=3.13"
# dependencies = ["requests"]
# ///"""

    update_file_with_metadata(script, metadata)

    updated_content = script.read_text()
    lines = updated_content.splitlines()
    assert lines[0] == "#!/usr/bin/env python3"
    assert "# /// script" in lines[1]


def test_update_file_replace_existing_metadata(tmp_path):
    """Test updating file that already has metadata."""
    script = tmp_path / "test_script.py"
    original_content = """#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["flask"]
# ///

import requests
print("Hello")
"""
    script.write_text(original_content)

    new_metadata = """# /// script
# requires-python = ">=3.13"
# dependencies = ["requests", "numpy"]
# ///"""

    update_file_with_metadata(script, new_metadata)

    updated_content = script.read_text()
    assert 'requires-python = ">=3.13"' in updated_content
    assert '"requests"' in updated_content
    assert '"numpy"' in updated_content
    assert '"flask"' not in updated_content
    assert 'requires-python = ">=3.11"' not in updated_content


def test_run_with_uv_success(mocker):
    """Test successful uv run execution."""
    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.return_value.returncode = 0

    script_path = Path("test_script.py")
    dependencies = ["requests", "numpy"]

    run_with_uv(script_path, dependencies)

    expected_cmd = [
        "uv",
        "run",
        "--with",
        "requests",
        "--with",
        "numpy",
        "test_script.py",
    ]
    mock_subprocess.assert_called_once_with(expected_cmd, check=True)


def test_run_with_uv_no_dependencies(mocker):
    """Test uv run with no dependencies."""
    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.return_value.returncode = 0

    script_path = Path("test_script.py")
    dependencies = []

    run_with_uv(script_path, dependencies)

    expected_cmd = ["uv", "run", "test_script.py"]
    mock_subprocess.assert_called_once_with(expected_cmd, check=True)


def test_run_with_uv_command_error(mocker):
    """Test uv run with command error."""
    from subprocess import CalledProcessError

    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.side_effect = CalledProcessError(1, "uv")

    script_path = Path("test_script.py")
    dependencies = ["requests"]

    with pytest.raises(SystemExit):
        run_with_uv(script_path, dependencies)


def test_run_with_uv_not_found(mocker):
    """Test uv run when uv is not installed."""
    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.side_effect = FileNotFoundError()

    script_path = Path("test_script.py")
    dependencies = ["requests"]

    with pytest.raises(SystemExit):
        run_with_uv(script_path, dependencies)


def test_check_uv_available_true(mocker):
    """Test check_uv_available when uv is available."""
    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.return_value.returncode = 0

    assert check_uv_available() is True


def test_check_uv_available_false_not_found(mocker):
    """Test check_uv_available when uv is not found."""
    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.side_effect = FileNotFoundError()

    assert check_uv_available() is False


def test_check_uv_available_false_error(mocker):
    """Test check_uv_available when uv returns error."""
    from subprocess import CalledProcessError

    mock_subprocess = mocker.patch("autopep723.subprocess.run")
    mock_subprocess.side_effect = CalledProcessError(1, "uv")

    assert check_uv_available() is False


def test_has_pep723_metadata_true(tmp_path):
    """Test has_pep723_metadata with script that has metadata."""
    script = tmp_path / "test_script.py"
    content = """# /// script
# requires-python = ">=3.13"
# dependencies = ["requests"]
# ///
import requests"""
    script.write_text(content)

    assert has_pep723_metadata(script) is True


def test_has_pep723_metadata_false(tmp_path):
    """Test has_pep723_metadata with script that doesn't have metadata."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    assert has_pep723_metadata(script) is False


def test_has_pep723_metadata_file_error():
    """Test has_pep723_metadata with non-existent file."""
    script = Path("nonexistent.py")
    assert has_pep723_metadata(script) is False


def test_import_mapping_contains_common_packages():
    """Test that the import mapping contains common packages."""
    assert IMPORT_TO_PACKAGE_MAP["bs4"] == "beautifulsoup4"
    assert IMPORT_TO_PACKAGE_MAP["PIL"] == "Pillow"
    assert IMPORT_TO_PACKAGE_MAP["cv2"] == "opencv-python"
    assert IMPORT_TO_PACKAGE_MAP["yaml"] == "PyYAML"
    assert IMPORT_TO_PACKAGE_MAP["sklearn"] == "scikit-learn"


def test_import_mapping_is_dict():
    """Test that import mapping is a dictionary."""
    assert isinstance(IMPORT_TO_PACKAGE_MAP, dict)
    assert len(IMPORT_TO_PACKAGE_MAP) > 0


def test_import_mapping_no_redundant_entries():
    """Test that import mapping doesn't contain redundant entries."""
    for import_name, package_name in IMPORT_TO_PACKAGE_MAP.items():
        # Import name should be different from package name
        assert import_name != package_name, f"Redundant entry: {import_name} -> {package_name}"


def test_full_workflow_simple_script(tmp_path):
    """Test the complete workflow with a simple script."""
    script = tmp_path / "test_script.py"
    script_content = """#!/usr/bin/env python3
import requests
import json
from bs4 import BeautifulSoup

response = requests.get("https://example.com")
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.title)
"""
    script.write_text(script_content)

    # Get imports
    imports = get_third_party_imports(script)

    # Generate metadata
    metadata = generate_pep723_metadata(imports)

    # Update file
    update_file_with_metadata(script, metadata)

    # Verify the result
    updated_content = script.read_text()

    assert "#!/usr/bin/env python3" in updated_content
    assert "# /// script" in updated_content
    assert '"requests"' in updated_content
    assert '"beautifulsoup4"' in updated_content
    # json should not be in dependencies (built-in module)
    assert '"json"' not in updated_content
    assert "import requests" in updated_content
    assert "from bs4 import BeautifulSoup" in updated_content


def test_workflow_with_existing_metadata(tmp_path):
    """Test workflow when script already has metadata."""
    script = tmp_path / "test_script.py"
    script_content = """#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["flask"]
# ///

import requests
import numpy as np
"""
    script.write_text(script_content)

    # Get imports
    imports = get_third_party_imports(script)

    # Generate new metadata
    metadata = generate_pep723_metadata(imports, ">=3.13")

    # Update file
    update_file_with_metadata(script, metadata)

    # Verify the result
    updated_content = script.read_text()

    assert '"requests"' in updated_content
    assert '"numpy"' in updated_content
    assert '"flask"' not in updated_content  # Should be replaced
    assert 'requires-python = ">=3.13"' in updated_content
    assert 'requires-python = ">=3.11"' not in updated_content


# URL functionality tests
def test_is_url():
    """Test URL detection function."""

    # Valid URLs
    assert is_url("https://example.com/script.py") is True
    assert is_url("http://localhost/test.py") is True
    assert is_url("ftp://server.com/file.py") is True

    # Invalid URLs
    assert is_url("script.py") is False
    assert is_url("/path/to/script.py") is False
    assert is_url("./relative/path.py") is False
    assert is_url("") is False
    assert is_url("not-a-url") is False


def test_resolve_script_path_local():
    """Test resolve_script_path with local files."""

    # Test with local path
    result = resolve_script_path("script.py")
    assert result == Path("script.py")

    result = resolve_script_path("/absolute/path.py")
    assert result == Path("/absolute/path.py")


def test_download_script(mocker, tmp_path):
    """Test script downloading functionality."""
    # Mock urllib.request.urlopen
    mock_response = mocker.Mock()
    mock_response.read.return_value = b'import requests\nprint("hello")'
    mock_response.__enter__ = mocker.Mock(return_value=mock_response)
    mock_response.__exit__ = mocker.Mock(return_value=None)

    mocker.patch("urllib.request.urlopen", return_value=mock_response)

    # Mock tempfile.NamedTemporaryFile
    temp_file = tmp_path / "autopep723_test.py"
    mock_file = mocker.Mock()
    mock_file.name = str(temp_file)
    mock_file.write = mocker.Mock()
    mock_file.__enter__ = mocker.Mock(return_value=mock_file)
    mock_file.__exit__ = mocker.Mock(return_value=None)

    mocker.patch("tempfile.NamedTemporaryFile", return_value=mock_file)

    # Test download
    url = "https://example.com/script.py"
    result = download_script(url)

    assert result == Path(tmp_path / "autopep723_test.py")


def test_resolve_script_path_url(mocker, tmp_path):
    """Test resolve_script_path with URLs."""
    # Mock urllib.request.urlopen
    mock_response = mocker.Mock()
    mock_response.read.return_value = b'import requests\nprint("hello")'
    mock_response.__enter__ = mocker.Mock(return_value=mock_response)
    mock_response.__exit__ = mocker.Mock(return_value=None)

    mocker.patch("urllib.request.urlopen", return_value=mock_response)

    # Mock tempfile.NamedTemporaryFile
    temp_file = tmp_path / "autopep723_test.py"
    temp_file.write_text('import requests\nprint("hello")')
    mock_file = mocker.Mock()
    mock_file.name = str(temp_file)
    mock_file.write = mocker.Mock()
    mock_file.__enter__ = mocker.Mock(return_value=mock_file)
    mock_file.__exit__ = mocker.Mock(return_value=None)

    mocker.patch("tempfile.NamedTemporaryFile", return_value=mock_file)

    # Test with URL
    url = "https://example.com/script.py"
    result = resolve_script_path(url)

    assert result == Path(tmp_path / "autopep723_test.py")


def test_download_script_error(mocker):
    """Test download_script error handling."""
    # Mock urllib.request.urlopen to raise an exception
    mocker.patch("urllib.request.urlopen", side_effect=Exception("Network error"))

    url = "https://example.com/script.py"

    with pytest.raises(SystemExit):
        download_script(url)


def test_is_url_error_handling():
    """Test is_url with malformed input that could cause exceptions."""
    # Test with None and other edge cases that might cause exceptions
    assert is_url(None) is False
    assert is_url(123) is False  # Non-string input
    assert is_url([]) is False  # List input


def test_get_third_party_imports_file_read_error(mocker, tmp_path):
    """Test get_third_party_imports when file read fails."""
    script = tmp_path / "test_script.py"
    script.write_text("import requests")

    # Mock pathlib Path.read_text to raise an exception
    mocker.patch.object(type(script), "read_text", side_effect=OSError("Permission denied"))

    imports = get_third_party_imports(script)
    assert imports == []
