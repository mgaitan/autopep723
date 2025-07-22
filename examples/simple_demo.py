#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def main():
    """Simple demo script that works without external dependencies."""

    print("🎯 autopep723 Demo Script")
    print("=" * 40)

    # Show system info
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Script path: {Path(__file__).absolute()}")
    print(f"Current time: {datetime.now().isoformat()}")

    # Create some sample data
    data = {
        "demo": "autopep723",
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version_info[:3],
        "features": [
            "Automatic dependency detection",
            "PEP 723 metadata generation",
            "Import name mapping",
            "File update capability",
            "Direct script execution",
        ],
    }

    # Display the data
    print("\n📊 Demo Data:")
    print(json.dumps(data, indent=2))

    # Test some built-in module functionality
    print("\n🔧 Testing built-in modules:")

    # Test pathlib
    current_file = Path(__file__)
    print(f"✓ pathlib: {current_file.name} ({current_file.stat().st_size} bytes)")

    # Test json
    json_str = json.dumps({"test": "data"})
    print(f"✓ json: Serialized {len(json_str)} characters")

    # Test datetime
    now = datetime.now()
    print(f"✓ datetime: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Test os
    env_count = len(os.environ)
    print(f"✓ os: Found {env_count} environment variables")

    print("\n✅ All tests completed successfully!")
    print("\nThis script demonstrates autopep723 with a script that:")
    print("  - Uses only built-in Python modules")
    print("  - Should generate empty dependencies list")
    print("  - Can be run without any external packages")
    print("\nTry running:")
    print("  autopep723 examples/simple_demo.py")
    print("  autopep723 add examples/simple_demo.py")
    print("  autopep723 check examples/simple_demo.py")


if __name__ == "__main__":
    main()
