#!/usr/bin/env autopep723
import json
from datetime import datetime

import requests


def main():
    """Example script that demonstrates shebang usage with autopep723."""

    print("🚀 Shebang Example Script")
    print("=" * 40)
    print("This script demonstrates using autopep723 as a shebang!")
    print()

    # Make a simple HTTP request
    try:
        print("📡 Making HTTP request to httpbin.org...")
        response = requests.get("https://httpbin.org/json", timeout=10)
        response.raise_for_status()

        data = response.json()
        print("✅ Request successful!")
        print(f"Response data: {json.dumps(data, indent=2)}")

    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return 1

    print()
    print("🎯 Key Points:")
    print("  - This script uses '#!/usr/bin/env autopep723' as shebang")
    print("  - autopep723 automatically detected 'requests' dependency")
    print("  - The script runs with: uv run --with requests script.py")
    print("  - No need to manually declare PEP 723 metadata!")

    print()
    print(f"⏰ Executed at: {datetime.now().isoformat()}")

    return 0

if __name__ == "__main__":
    exit(main())
