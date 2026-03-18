import json
import os
from datetime import date
from dotenv import load_dotenv

# Optional imports based on provider
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

SYSTEM_PROMPT = """
You are an Advanced Invoice Processing Agent. Your goal is to extract structured data from invoice text with 100% precision.

### Rules:
1. Extract all core fields: Vendor, Invoice Number, Date, Tax, Total.
2. Line Items: Extract description, quantity (if available), unit_price (if available), and total_amount for each item.
3. Validation:
   - Calculate if (Sum of Line Item Amounts + Tax) matches the Total.
   - Flag any mathematical inconsistencies.
   - Flag if the date format is unusual or future-dated.
   - Flag missing critical information (e.g., missing invoice number).
4. Do not guess values. If a value is missing, return null.

Return ONLY a valid JSON object:
{
  "vendor": "string",
  "invoice_number": "string",
  "invoice_date": "string",
  "line_items": [
    {
      "description": "string",
      "quantity": number or null,
      "unit_price": number or null,
      "amount": number
    }
  ],
  "tax": number,
  "total": number,
  "currency": "string",
  "validation_results": {
    "math_check_passed": boolean,
    "calculated_total": number,
    "discrepancy": number,
    "flags": ["string"]
  },
  "financial_summary": "string"
}
"""

def process_invoice(prompt_text, provider="OpenAI", model=None, api_key=None):
    if provider == "OpenAI":
        return _call_openai(prompt_text, model or "gpt-4o-mini", api_key)
    elif provider == "Anthropic":
        return _call_anthropic(prompt_text, model or "claude-3-5-sonnet-20240620", api_key)
    elif provider == "Gemini":
        return _call_gemini(prompt_text, model or "gemini-1.5-flash", api_key)
    elif provider == "Groq":
        return _call_groq(prompt_text, model or "llama-3.1-70b-versatile", api_key)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def _call_openai(prompt, model, api_key):
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    return json.loads(response.choices[0].message.content)

def _call_anthropic(prompt, model, api_key):
    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return json.loads(response.content[0].text)

def _call_gemini(prompt, model, api_key):
    genai.configure(api_key=api_key or os.getenv("GEMINI_API_KEY"))
    model_instance = genai.GenerativeModel(
        model_name=model,
        system_instruction=SYSTEM_PROMPT
    )
    response = model_instance.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    return json.loads(response.text)

def _call_groq(prompt, model, api_key):
    client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data, base_path=""):
    json_path = os.path.join(base_path, "invoice.json")
    txt_path = os.path.join(base_path, "invoice.txt")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"ADVANCED INVOICE ANALYSIS ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Vendor: {data.get('vendor')}\n")
        f.write(f"Invoice #: {data.get('invoice_number')}\n")
        f.write(f"Date: {data.get('invoice_date')}\n")
        f.write(f"Currency: {data.get('currency')}\n\n")
        
        f.write("Line Items:\n")
        for item in data.get("line_items", []):
            qty = item.get('quantity') or 1
            price = item.get('unit_price') or item.get('amount')
            f.write(f"- {item['description']} (x{qty}): {price}\n")
            
        f.write(f"\nTax: {data.get('tax')}\n")
        f.write(f"Total: {data.get('total')}\n")
        f.write("-" * 30 + "\n")
        
        val = data.get('validation_results', {})
        f.write(f"Validation: {'PASSED' if val.get('math_check_passed') else 'FAILED'}\n")
        for flag in val.get('flags', []):
            f.write(f"🚩 FLAG: {flag}\n")
            
        f.write(f"\nSummary: {data.get('financial_summary')}\n")

def process_invoice_batch(texts, provider="OpenAI", model=None, api_key=None):
    results = []
    for text in texts:
        results.append(process_invoice(text, provider, model, api_key))
    return results

def main():
    if not os.path.exists("input.txt"):
        print("Error: input.txt not found.")
        return
        
    with open("input.txt", "r", encoding="utf-8") as f:
        context = f.read()
        
    try:
        print("Processing invoice via default provider...")
        result = process_invoice(context)
        save_outputs(result)
        print("Success! invoice.json and invoice.txt generated.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
