from pathlib import Path

for file in Path(".").rglob("*.txt"):
    print(file)

for file in Path(".").rglob("*.py"):
    print(file)

for file in Path(".").rglob("*.json"):
    print(file)