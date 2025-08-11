import sys

# check date argument
if len(sys.argv) != 2:
    print("❗ Use: python3 file_checker.py <data> (example 20250809 or 09-08-2025)")
    sys.exit(1)

# Take date from argument
date_input = sys.argv[1]

print(f"Received date argument: {date_input}")
