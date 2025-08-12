import os
import datetime

with os.scandir(".") as entries:
    for entry in entries:
        if entry.is_file() and entry.name.endswith(".txt"):
            created = datetime.datetime.fromtimestamp(entry.stat().st_birthtime)
            
            with open(entry.path, "r", encoding="utf-8") as f:
                line_count = sum(1 for _ in f)

            print(f"{entry.name} -> {line_count} lines, created {created}")
