import os
import re

readme_path = r"h:\100 AI Agents\README.md"
root_dir = r"h:\100 AI Agents"

with open(readme_path, "r", encoding="utf-8") as f:
    text = f.read()

# Extract relative paths from README links
paths = re.findall(r"\[.*?\]\((.*?)\)", text)
agent_dirs = [p[p.find("./")+2:] for p in paths if p.startswith("./")]

print(f"Diagnostics: Found {len(agent_dirs)} agent directories in README.")

results = []
for adir in agent_dirs:
    full_path = os.path.join(root_dir, adir.replace("%20", " "))
    if not os.path.exists(full_path):
        results.append(f"❌ MISSED DIR: {adir}")
        continue
    
    files = os.listdir(full_path)
    has_agent = "agent.py" in files
    has_app = "app.py" in files
    has_reqs = "requirements.txt" in files
    
    status = ""
    if not has_agent: status += " NO_AGENT"
    if not has_app: status += " NO_APP"
    if not has_reqs: status += " NO_REQS"
    
    if status:
        results.append(f"⚠️ {adir}: {status}")
    else:
        results.append(f"✅ {adir}: FULLY_WORKING")

for res in results:
    print(res)
