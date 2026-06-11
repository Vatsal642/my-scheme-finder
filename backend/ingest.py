from scraper import scrape_schemes
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import json, os

# Free local embeddings — no API key required
EMBEDDINGS_MODEL = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def build_index():
    # Load schemes
    if os.path.exists("schemes.json"):
        with open("schemes.json") as f:
            schemes = json.load(f)
    else:
        schemes = scrape_schemes()
        if schemes:
            with open("schemes.json", "w", encoding="utf-8") as f:
                json.dump(schemes, f, indent=2)

    # Convert to Documents
    docs = []
    for s in schemes:
        content = f"""
Scheme Name: {s['name']}
Ministry: {s['ministry']}
Description: {s['description']}
Eligibility: {s['eligibility']}
Benefits: {s['benefits']}
How to Apply: {s['how_to_apply']}
Target Group: {s['target_group']}
State: {s['state']}
Official URL: {s['url']}
""".strip()
        docs.append(Document(
            page_content=content,
            metadata={
                "name": s["name"],
                "ministry": s["ministry"],
                "category": s.get("category", "general"),
                "state": s["state"],
                "url": s["url"],
                "target_group": s["target_group"]
            }
        ))

    if not docs:
        print("No documents to index.")
        return None

    # Chunk
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80
    )
    chunks = splitter.split_documents(docs)

    # Embed and store using free local model
    vectorstore = FAISS.from_documents(chunks, EMBEDDINGS_MODEL)
    vectorstore.save_local("faiss_index")
    print(f"Indexed {len(chunks)} chunks from {len(schemes)} schemes.")
    return vectorstore

if __name__ == "__main__":
    build_index()
