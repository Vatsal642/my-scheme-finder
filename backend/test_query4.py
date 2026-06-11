import os
from dotenv import load_dotenv
load_dotenv()
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

from rag import load_retriever

print("Loading retriever...")
retriever = load_retriever()

print("Testing retriever directly...")
docs = retriever.invoke("I am a 32 year old woman farmer")
print(f"Retriever worked! Found {len(docs)} docs.")
