import os

root_dir = r"h:\100 AI Agents"
standard_reqs = "openai\nlitellm\nstreamlit\npandas\npython-dotenv\n"

agents_fixed = 0
for root, dirs, files in os.walk(root_dir):
    # Detect an agent directory
    if "agent.py" in files or "app.py" in files:
        # Ignore some dirs like .git, __pycache__, etc. (though walk ignores them mostly)
        if any(x in root for x in [".git", "__pycache__", ".ipynb_checkpoints"]):
            continue
            
        req_path = os.path.join(root, "requirements.txt")
        if not os.path.exists(req_path):
            with open(req_path, "w", encoding="utf-8") as f:
                f.write(standard_reqs)
            agents_fixed += 1
            print(f"Added requirements.txt to: {root}")

print(f"Audit Complete. Added requirements.txt to {agents_fixed} agent(s).")
