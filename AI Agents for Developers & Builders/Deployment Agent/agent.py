import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()

def deploy_project(project, stack, platform="Render (Free Tier)", enable_k8s=False, model="gpt-4o-mini"):
    """
    Generates a complete, production-grade deployment plan for any project.
    """
    k8s_instruction = "\nInclude a Kubernetes Deployment + Service manifest." if enable_k8s else "\nSet kubernetes_manifest to 'N/A'."

    user_prompt = f"""
PROJECT DESCRIPTION:
{project}

TECH STACK:
{stack}

TARGET DEPLOYMENT PLATFORM: {platform}

{k8s_instruction}

Generate the full deployment plan including Dockerfile, docker-compose, GitHub Actions CI/CD YAML,
environment variables, deployment steps, cost estimate, and security checklist.
"""
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {
            "error": str(e),
            "message": "Deployment engine failure. Check API key and model availability."
        }
