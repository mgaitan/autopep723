import sys

print("All arguments:", sys.argv)
print("Script arguments:", sys.argv[1:])
if len(sys.argv) > 1:
    print("First argument:", sys.argv[1])
