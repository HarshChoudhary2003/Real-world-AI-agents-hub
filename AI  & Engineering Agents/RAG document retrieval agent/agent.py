import json
import numpy as np
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

def embed(text, model="text-embedding-3-small"):
    """Generates embeddings via LiteLLM."""
    response = litellm.embedding(
        model=model,
        input=[text]
    )
    return np.array(response.data[0]['embedding'])

def cosine_similarity(a, b):
    """Computes similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def load_documents(path="documents.txt"):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f.readlines() if l.strip()]

def load_query(path="query.txt"):
    if not os.path.exists(path):
        return "Query missing"
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def retrieve(docs, query, top_k=2):
    if not docs:
        return []
    
    query_vec = embed(query)
    scored = []

    for d in docs:
        vec = embed(d)
        score = cosine_similarity(query_vec, vec)
        scored.append((d, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]

def save_outputs(results):
    payload = {
        "date": str(date.today()),
        "status": "success",
        "results": [
            {"document": r[0], "similarity": round(float(r[1]), 3)}
            for r in results
        ]
    }

    with open("retrieved_context.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    with open("retrieved_context.txt", "w", encoding="utf-8") as f:
        f.write(f"RAG Semantic Retrieval Report ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write("Candidate Documents Found:\n")
        for r in payload["results"]:
            f.write(f"Score: {r['similarity']} | Doc: {r['document']}\n")

def main():
    print("🚀 SemanticForge AI: Orchestrating RAG Retrieval...")
    try:
        docs = load_documents()
        query = load_query()
        if not docs:
            print("⚠️ No documents found in documents.txt")
            return
            
        results = retrieve(docs, query)
        save_outputs(results)
        print("✅ RAG document retrieval completed.")
        print("📁 Outputs: retrieved_context.json, retrieved_context.txt")
    except Exception as e:
        print(f"❌ Logic fail: {str(e)}")

if __name__ == "__main__":
    main()
