import json
import numpy as np
from openai import OpenAI
from datetime import date
import os
import sys
 
client = None
if os.getenv("OPENAI_API_KEY"):
    try:
        client = OpenAI()
    except Exception:
        pass

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
 
 
def read_notes(path="notes.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]
 
 
def embed_texts(texts):
    if client is None:
        raise ValueError("OpenAI client not initialized.")
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts
    )
    return [e.embedding for e in response.data]
 
 
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    # prevent divide by zero
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))
 
 
def store_knowledge(chunks, embeddings):
    records = []
    for text, emb in zip(chunks, embeddings):
        records.append({
            "text": text,
            "embedding": emb,
            "created": date.today().isoformat()
        })
    with open("knowledge.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    return records
 
 
def load_knowledge():
    with open("knowledge.json", "r", encoding="utf-8") as f:
        return json.load(f)
 
 
def retrieve(query, records, top_k=3):
    query_emb = embed_texts([query])[0]
    scored = []
    for r in records:
        score = cosine_similarity(query_emb, r["embedding"])
        scored.append((score, r["text"]))
    scored.sort(reverse=True)
    return [text for _, text in scored[:top_k]]
 
 
def answer_query(query, contexts):
    if client is None:
        return "OpenAI client not initialized. Cannot answer query."
    prompt = f"""
You are a highly capable and intelligent AI assistant. 
First, try to answer the question using the provided Notes from the user's personal knowledge base.
If the Notes do not contain the answer, or if the user asks a general question, you MUST use your own vast general knowledge to answer the question fully and accurately.
Always be helpful, detailed, and powerful.
 
Notes from Personal Knowledge Base:
{chr(10).join(contexts)}
 
Question:
{query}
"""
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content
 
 
def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set.")
        
    print("Ingesting notes...")
    try:
        chunks = read_notes()
        embeddings = embed_texts(chunks)
        records = store_knowledge(chunks, embeddings)
    except Exception as e:
        print(f"Error during ingestion: {e}")
        return

    print("Knowledge base ready.")
    
    # Let script read from argument if provided, to easily test from script without interactive TTY
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"\nAsk a question: {query}")
    else:
        query = input("\nAsk a question: ")
        
    top_contexts = retrieve(query, records)
    answer = answer_query(query, top_contexts)
 
    print("\nAnswer:")
    print(answer)
 
 
if __name__ == "__main__":
    main()
