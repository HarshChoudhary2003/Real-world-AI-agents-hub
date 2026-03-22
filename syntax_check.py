import os
import ast

root_dir = r"h:\100 AI Agents"
errors = []

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            if any(x in path for x in [".git", "__pycache__", "venv"]):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    ast.parse(f.read())
            except Exception as e:
                errors.append(f"{path}: {str(e)}")

if errors:
    print("Found Syntax Errors:")
    for err in errors:
        print(err)
else:
    print("All python modules are syntactically correct.")
