import os

def update_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # Skip .git, .gemini, venv, etc.
        if any(skip in root for skip in ['.git', '.gemini', 'venv', '__pycache__']):
            continue

        # Update app.py
        if 'app.py' in files:
            path = os.path.join(root, 'app.py')
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if already has branding
            if 'Developed by Harsh' not in content and 'Developed with ❤️ by Harsh' not in content:
                # Append to the end or before last block
                # Simplest: check if there is a sidebar block
                if 'with st.sidebar:' in content:
                    # Find the last line of the sidebar content if possible or just append to the file
                    content += '\n\nwith st.sidebar:\n    st.markdown("---")\n    st.caption("Developed by Harsh")\n'
                else:
                    content += '\n\nst.markdown("---")\nst.caption("Developed by Harsh")\n'
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {path}")

        # Update README.md
        if 'README.md' in files:
            path = os.path.join(root, 'README.md')
            # Don't update the root README.md here, or handle it specifically
            if path == os.path.join(root_dir, 'README.md'):
                # Add to the very end of root README if not present
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'Developed with ❤️ by [Harsh Choudhary]' not in content:
                    content += '\n\n---\n\nDeveloped with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003)\n'
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                continue

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'Developed with ❤️ by' not in content and 'Developed by Harsh' not in content:
                content += '\n\n---\n\nDeveloped with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*\n'
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {path}")

if __name__ == "__main__":
    update_files('h:/100 AI Agents')
