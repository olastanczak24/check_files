# This script parses "check_files" scan results, groups them by directory and file type,
# and then compares yesterday’s file line counts with historical medians.
# Steps:
# 1. Parse raw scan output (normalize, extract folders, filenames, line counts).
# 2. Group results by directory and by file type prefix.
# 3. For each file type, find yesterday’s entry (based on YYYYMMDD in filename).
# 4. Compute the median of all other entries for comparison.
# 5. Print per-folder summaries showing yesterday’s values and the historical median.

import os
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
import re

# <<< check_files results >>>
raw = """ """
#use """Checking: <pattern> in <directory> <DATE> → Match: <filename> → Lines: <number>"""

# precent day(YYYYMMDD)
prev_date = (datetime.now().date() - timedelta(days=1)).strftime("%Y%m%d")

# --- PARSER: ---
norm = raw.replace("→", "->")
results = []
current_folder = None
re_checking = re.compile(r'^Checking:.* in (.+)$')
re_match    = re.compile(r'^\s*\d{8}.*?Match:\s*(\S+).*?Lines:\s*(\d+)', re.IGNORECASE)

for line in norm.splitlines():
    s = line.strip()
    if not s:
        continue
    m = re_checking.match(s)
    if m:
        current_folder = m.group(1).strip()
        continue
    if "No matching file found" in s:
        continue
    m = re_match.match(s)
    if m and current_folder:
        filename = m.group(1)
        nlines = int(m.group(2))
        results.append((os.path.join(current_folder, filename), nlines))
# --- End of parsing ---

# groups with directories
groups = defaultdict(list)
for fp, n in results:
    groups[os.path.dirname(fp)].append((fp, n))

# printing
for folder, items in groups.items():
    # (YYYYMMDD)
    by_type = defaultdict(list)
    for fp, n in items:
        name = os.path.basename(fp)
        m = re.search(r'(\d{8})', name)
        left = name.split(m.group(1))[0] if m else os.path.splitext(name)[0]
        ftype = left.rstrip('_')  # usage: 'exa_cpu', 'exa_storage',
        by_type[ftype].append((fp, n))

    
    for ftype, titems in by_type.items():
        prev_entries = []
        rest = []
        for fp, n in titems:
            m = re.search(r'(\d{8})', os.path.basename(fp))
            if m and m.group(1) == prev_date:
                prev_entries.append(f"{os.path.basename(fp)} = {n}")
            else:
                rest.append(n)

        med = statistics.median(rest) if rest else 0

      
        if prev_entries:
            print(f"{folder} | {ftype} | yesterday: {', '.join(prev_entries)}")
        else:
            print(f"{folder} | {ftype} | yesterday: (no {prev_date}) = 0")
        print(f"{folder} | {ftype} | median: {med}\n")
