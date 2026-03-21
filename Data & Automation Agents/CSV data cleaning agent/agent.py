import pandas as pd
import json
import os
import glob
import numpy as np
from datetime import date
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# --- AI Orchestration: LiteLLM + Instructor ---
import litellm
try:
    import instructor
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

load_dotenv()

# --- Structured Pydantic Models ---
class DataIssue(BaseModel):
    column: str
    original_value: Any
    suggested_value: Any
    reason: str

class SemanticRefinement(BaseModel):
    refined_row: Dict[str, Any]
    issues_fixed: List[DataIssue]

# --- Helper for JSON Serialization ---
def safe_json_serialize(obj):
    if isinstance(obj, (np.int64, np.int32, np.integer)): return int(obj)
    if isinstance(obj, (np.float64, np.float32, np.floating)): return float(obj)
    if isinstance(obj, (pd.Timestamp, date)): return str(obj)
    if isinstance(obj, dict): return {k: safe_json_serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, pd.Series, pd.Index)): return [safe_json_serialize(i) for i in obj]
    return obj

# --- Universal AI Logic Hub ---
def semantic_refine_row(row_dict: Dict[str, Any], rules: List[str], model: str, api_key: Optional[str] = None) -> SemanticRefinement:
    if not LLM_AVAILABLE: return SemanticRefinement(refined_row=row_dict, issues_fixed=[])
    client = instructor.from_litellm(litellm.completion)
    rules_str = "\n".join([f"- {r}" for r in rules])
    prompt = f"Analyze row data and apply validation rules: {rules_str}\nData: {json.dumps(row_dict)}"
    try:
        return client.chat.completions.create(
            model=model,
            response_model=SemanticRefinement,
            messages=[{"role": "user", "content": prompt}],
            api_key=api_key
        )
    except: return SemanticRefinement(refined_row=row_dict, issues_fixed=[])

# --- Advanced Cleaning Core ---
class AdvancedCSVCleaner:
    def __init__(self, df: pd.DataFrame, filename: str = "unknown"):
        self.filename = filename
        self.raw_df = df.copy()
        self.df = df.copy()
        self.custom_rules = []
        self.report = {
            "filename": filename,
            "missing_values_before": self.raw_df.isnull().sum().to_dict(),
            "duplicates_removed": 0,
            "rule_violations": [],
            "llm_refinements": []
        }

    def add_custom_rule(self, column: str, operator: str, value: Any, description: str):
        self.custom_rules.append({"column": column, "operator": operator, "value": value, "description": description})

    def apply_custom_rules(self):
        for rule in self.custom_rules:
            col = rule["column"]
            if col not in self.df.columns: continue
            if rule["operator"] == "range":
                min_v, max_v = rule["value"]
                temp_col = pd.to_numeric(self.df[col], errors='coerce')
                violations = self.df[(temp_col < min_v) | (temp_col > max_v)]
                for idx in violations.index:
                    self.report["rule_violations"].append({"row": int(idx), "column": col, "value": str(self.df.loc[idx, col]), "rule": f"Range {min_v}-{max_v}"})
                self.df.loc[violations.index, col] = None
            elif rule["operator"] == "regex":
                violations = self.df[~self.df[col].astype(str).str.contains(str(rule["value"]), na=False)]
                for idx in violations.index:
                    self.report["rule_violations"].append({"row": int(idx), "column": col, "value": str(self.df.loc[idx, col]), "rule": f"Regex: {rule['description']}"})

    def final_pipeline(self, ai_model: Optional[str] = None, api_key: Optional[str] = None):
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        self.report["duplicates_removed"] = int(before - len(self.df))
        for col in self.df.columns:
            if "date" in col.lower(): self.df[col] = pd.to_datetime(self.df[col], errors="coerce").dt.strftime('%Y-%m-%d')
        self.apply_custom_rules()
        if ai_model and api_key:
            sample = self.df.head(10).copy()
            rules_for_ai = [f"{r['column']} must satisfy: {r['description']}" for r in self.custom_rules]
            refined = []
            for _, row in sample.iterrows():
                res = semantic_refine_row(row.to_dict(), rules_for_ai, ai_model, api_key)
                refined.append(res.refined_row)
                for issue in res.issues_fixed: self.report["llm_refinements"].append(issue.dict())
            self.df.update(pd.DataFrame(refined))

    def finalize_report(self) -> Dict[str, Any]:
        self.report["missing_values_after"] = self.df.isnull().sum().to_dict()
        self.report["date_processed"] = str(date.today())
        total_cells = int(self.raw_df.size) if self.raw_df.size > 0 else 1
        issues_count = sum(self.report["missing_values_before"].values()) + self.report["duplicates_removed"] + len(self.report["rule_violations"])
        self.report["health_score"] = round(float(max(0, 100 * (1 - (issues_count / total_cells)))), 2)
        return safe_json_serialize(self.report)

# --- Batch Processing Matrix ---
class NeuralBatchProcessor:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.individual_reports = []

    def run_batch(self, rules: List[Dict[str, Any]], ai_model: Optional[str] = None, api_key: Optional[str] = None):
        files = glob.glob(os.path.join(self.input_dir, "raw_data*.csv"))
        print(f"📂 Neural Batch Hub: Found {len(files)} target matrices.")
        for fpath in files:
            fname = os.path.basename(fpath)
            print(f"➡️ Processing {fname}...")
            df = pd.read_csv(fpath)
            cleaner = AdvancedCSVCleaner(df, fname)
            for r in rules: cleaner.add_custom_rule(r["column"], r["operator"], r["value"], r["description"])
            cleaner.final_pipeline(ai_model=ai_model, api_key=api_key)
            report = cleaner.finalize_report()
            self.individual_reports.append(report)
            cleaner.df.to_csv(os.path.join(self.output_dir, f"cleaned_{fname}"), index=False)
        agg_score = sum(r.get("health_score", 0) for r in self.individual_reports) / len(self.individual_reports) if self.individual_reports else 0
        print(f"✅ Batch complete. Aggregate Score: {agg_score:.1f}%")
        batch_summary = {"date": str(date.today()), "total_files": len(files), "aggregate_health_score": round(float(agg_score), 2), "files": self.individual_reports}
        with open(os.path.join(self.output_dir, "batch_report.json"), "w", encoding="utf-8") as f: json.dump(batch_summary, f, indent=2)

if __name__ == "__main__":
    rules = [{"column": "age", "operator": "range", "value": [0, 120], "description": "valid age"}]
    processor = NeuralBatchProcessor("./", "./cleaned_batch")
    processor.run_batch(rules, ai_model=None)
