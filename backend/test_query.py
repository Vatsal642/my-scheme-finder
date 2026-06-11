import os
from dotenv import load_dotenv
load_dotenv()
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from rag import load_retriever, get_qa_chain, query_schemes

print("Loading retriever...")
retriever = load_retriever()
print("Loading QA chain...")
qa_chain = get_qa_chain(retriever)
print("Querying...")
res = query_schemes(qa_chain, "I am a 32 year old woman farmer")
print(res)
print("Success!")
