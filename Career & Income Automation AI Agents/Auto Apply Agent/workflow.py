import sys
import os

# Dynamic path resolution for sibling agents
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESUME_AGENT_PATH = os.path.join(BASE_DIR, "Resume Optimizer Agent")
COVER_LETTER_AGENT_PATH = os.path.join(BASE_DIR, "Cover Letter Generator Agent")

# Add paths to sys.path if not present
if RESUME_AGENT_PATH not in sys.path: sys.path.append(RESUME_AGENT_PATH)
if COVER_LETTER_AGENT_PATH not in sys.path: sys.path.append(COVER_LETTER_AGENT_PATH)

try:
    from agent import ResumeOptimizerAgent as ResumeAgent  # From Resume Optimizer Agent folder
except ImportError:
    ResumeAgent = None

try:
    from agent import generate_cover_letter as generate_cl  # From Cover Letter Generator Agent folder
except ImportError:
    generate_cl = None

def run_auto_apply_workflow(resume, job_desc, company, api_key=None, ai_model="gpt-4o-mini"):
    """
    Orchestrates the multi-agent application pipeline.
    1. Optimize Resume -> 2. Generate Cover Letter -> 3. Combine Score
    """
    
    # 1. Optimize Resume
    optimized_resume_text = resume
    match_score = 0
    detailed_analysis = ""
    
    if ResumeAgent:
        # We assume ResumeAgent uses OpenAI since we just pushed keys there
        # but we handle defaults gracefully
        try:
            opt_agent = ResumeAgent() # Default provider/model
            optimization_result = opt_agent.optimize(resume, job_desc)
            optimized_resume_text = optimization_result.get("optimized_resume", resume)
            match_score = optimization_result.get("match_score", 0)
            detailed_analysis = optimization_result.get("analysis", "")
        except Exception as e:
            print(f"Workflow Warning (Resume): {str(e)}")
    
    # 2. Generate Cover Letter using the Optimized Resume context
    cover_letter = "Generating cover letter..."
    if generate_cl:
        try:
            cover_letter = generate_cl(
                resume=optimized_resume_text, 
                job_description=job_desc, 
                company=company,
                model=ai_model,
                api_key=api_key # Use the same key for the whole session
            )
        except Exception as e:
            cover_letter = f"Workflow Warning (Cover Letter): {str(e)}"
            
    return {
        "optimized_resume": optimized_resume_text,
        "cover_letter": cover_letter,
        "match_score": match_score,
        "analysis": detailed_analysis
    }
