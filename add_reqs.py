import os

base_dir = r"h:\100 AI Agents"
target_dirs = ["AI  & Engineering Agents", "HR , Legal & Compliance Agents"]

default_reqs = """openai
litellm
streamlit
pandas
python-dotenv
"""

candidate_reqs = """openai
litellm
streamlit
pandas
python-dotenv
PyPDF2
python-docx
"""

count = 0
for t in target_dirs:
    full_target = os.path.join(base_dir, t)
    if os.path.exists(full_target):
        for root, dirs, files in os.walk(full_target):
            # Only go one level deep to the agent directories
            depth = root[len(full_target):].count(os.sep)
            if depth == 1:
                if "agent.py" in files or "app.py" in files:
                    req_path = os.path.join(root, "requirements.txt")
                    reqs = candidate_reqs if "Candidate screening agent" in root else default_reqs
                    with open(req_path, "w", encoding="utf-8") as f:
                        f.write(reqs)
                    count += 1

print(f"Added requirements.txt to {count} agent directories.")
