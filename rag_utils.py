# rag_utils.py
import pandas as pd
import faiss
import numpy as np
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_dataset(filepath):
    df = pd.read_excel(filepath, engine="openpyxl")
    return df

def row_to_text(row):
    return ", ".join([f"{col}: {val}" for col, val in row.items()])

def embed_text(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [r.embedding for r in response.data]

def build_faiss_index(df):
    texts = df.apply(row_to_text, axis=1).tolist()
    embeddings = embed_text(texts)
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index, texts
