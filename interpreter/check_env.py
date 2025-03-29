import sys
import os
import site

print("=" * 40)
print("Python Version:", sys.version)
print("Python Executable:", sys.executable)
print("=" * 40)

print("\nSYSPATH:")
for p in sys.path:
    print(f"  {p}")
print("=" * 40)

print("\nENVIRONMENT VARIABLES:")
for key, value in sorted(os.environ.items()):
    if "PATH" in key or "PYTHON" in key.upper():
        print(f"  {key}: {value}")
print("=" * 40)

print("\nDEBUG - Attempting to find 'google' package:")
possible_paths = []
for path in sys.path:
    google_path = os.path.join(path, "google")
    if os.path.exists(google_path):
        possible_paths.append(google_path)
        print(f"  Found google package at: {google_path}")
        # List contents
        print(f"  Contents: {os.listdir(google_path)}")

if not possible_paths:
    print("  No 'google' package found in sys.path")

print("=" * 40)
