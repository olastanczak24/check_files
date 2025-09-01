import os
import statistics

def count_lines(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return sum(1 for _ in f) 
    
folder_path = "your/path/to/directory"
files = os.listdir(folder_path)

line_counts = []

for file in files:
    if file.endswith(".txt") or file.endswith(".csv"):
        filepath = os.path.join(folder_path, file)
        lines = count_lines(filepath)
        line_counts.append(lines)
        print(f"File {file} has {lines} lines.")

if line_counts:
    median_value = statistics.median(line_counts)
    print(f"Median value is {median_value}")
