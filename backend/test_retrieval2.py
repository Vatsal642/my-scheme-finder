from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

query1 = "I am a 28 year old woman farmer from UP, income below 1.5 lakh"
docs1 = vectorstore.similarity_search(query1, k=25)
for i, d in enumerate(docs1):
    print(f"{i+1}. {d.metadata.get('name')}")
