import json
import os
from openai import OpenAI
from google import generativeai as genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ResumeOptimizerAgent:
    def __init__(self, provider="OpenAI", model="gpt-4o-mini"):
        self.provider = provider
        self.model = model
        
    def _openai_call(self, resume, job_description):
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Optimize the following resume for this job description:\n\nRESUME:\n{resume}\n\nJOB DESCRIPTION:\n{job_description}"}
            ],
            response_format={ "type": "json_object" },
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)

    def _gemini_call(self, resume, job_description):
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=SYSTEM_PROMPT
        )
        prompt = f"Optimize the following resume for this job description:\n\nRESUME:\n{resume}\n\nJOB DESCRIPTION:\n{job_description}\n\nReturn ONLY valid JSON."
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)

    def optimize(self, resume, job_description):
        if self.provider == "OpenAI":
            return self._openai_call(resume, job_description)
        elif self.provider == "Google Gemini":
            return self._gemini_call(resume, job_description)
        else:
            raise ValueError(f"Provider {self.provider} not supported.")

if __name__ == "__main__":
    # Internal CLI test
    agent = ResumeOptimizerAgent()
    sample_resume = "Software Engineer with 2 years of experience."
    sample_jd = "Senior React Developer needed."
    print(json.dumps(agent.optimize(sample_resume, sample_jd), indent=2))
