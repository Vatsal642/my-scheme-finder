import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from rag import load_retriever, get_qa_chain, EMBEDDINGS_MODEL
from langchain_groq import ChatGroq

print("Testing embeddings...")
emb = EMBEDDINGS_MODEL.embed_query("test")
print("Embeddings worked! Length:", len(emb))

print("Testing ChatGroq...")
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
res = llm.invoke("Say hello")
print("Groq worked! Response:", res)

print("Loading retriever...")
retriever = load_retriever()
print("Testing retriever directly...")
docs = retriever.invoke("I am a 32 year old woman farmer")
print(f"Retriever worked! Found {len(docs)} docs.")

print("Success!")
