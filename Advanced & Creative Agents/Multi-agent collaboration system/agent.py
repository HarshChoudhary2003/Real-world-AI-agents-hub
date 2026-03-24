import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY in environment

def call_agent(role, task):
    """
    Standard agent call using specialized system prompts.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a {role}. Provide clear, professional, and actionable output."},
                {"role": "user", "content": task}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling {role}: {str(e)}"

def main():
    print("Initializing Multi-Agent Collaboration System...")
    
    # Task 1: Research
    print("Step 1: Research Agent is gathering data...")
    research_output = call_agent("Research Agent", "Summarize current market trends for AI-driven productivity tools in 2025-2026.")
    
    # Task 2: Analysis
    print("Step 2: Analysis Agent is processing research...")
    analysis_output = call_agent("Analysis Agent", f"Analyze this research and identify 3 strategic opportunities:\n{research_output}")
    
    # Aggregate Output
    output = {
        "research_agent_output": research_output,
        "analysis_agent_output": analysis_output,
        "final_summary": analysis_output
    }
    
    # Save results
    output_path = os.path.join(os.path.dirname(__file__), "multi_agent_output.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nMulti-agent collaboration completed. Results saved to {output_path}")

if __name__ == "__main__":
    main()
