#!/usr/bin/env python3
"""Test script to verify argument passing works correctly with autopep723."""

import json
import sys


def main():
    """Test different argument scenarios."""
    print("🧪 Testing autopep723 argument passing")
    print("=" * 50)

    # Show all arguments received
    print(f"Total arguments received: {len(sys.argv) - 1}")
    print(f"Script name: {sys.argv[0]}")

    if len(sys.argv) > 1:
        print(f"Arguments: {sys.argv[1:]}")

        # Test different argument types
        for i, arg in enumerate(sys.argv[1:], 1):
            print(f"  Arg {i}: '{arg}' (type: {type(arg).__name__})")

            # Check for different patterns
            if arg.startswith("--"):
                print("    → Long flag detected")
            elif arg.startswith("-"):
                print("    → Short flag detected")
            elif arg.isdigit():
                print(f"    → Numeric argument: {int(arg)}")
            elif " " in arg:
                print("    → Multi-word argument detected")
            else:
                print("    → Regular argument")
    else:
        print("No arguments received")

    # Test JSON serialization of arguments (useful for complex data)
    try:
        args_json = json.dumps(sys.argv[1:])
        print(f"\nArguments as JSON: {args_json}")
    except Exception as e:
        print(f"Could not serialize arguments as JSON: {e}")

    print("\n✅ Test completed successfully!")


if __name__ == "__main__":
    main()
