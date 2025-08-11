import os

ROOT = "."

if not os.path.exists(ROOT):
    print(f"Dir '{ROOT}' not exist.")
    exit(1)
    
print(f"Content of directory '{ROOT}':")
for filename in os.listdir(ROOT):
    file_path = os.path.join(ROOT, filename)
    if os.path.isfile(file_path):
        print(f" {filename}")
