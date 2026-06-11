from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
import os

# Free local embeddings — no API key required
EMBEDDINGS_MODEL = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

SYSTEM_PROMPT = """
You are a helpful and empathetic Indian government scheme advisor. 
A citizen has described their personal situation. Using ONLY the 
scheme information provided below, identify which schemes they 
are most likely eligible for.

For each matching scheme, provide:
1. **Scheme name** (bold)
2. Why this person qualifies (specific to what they told you)
3. Key benefit they will receive
4. How to apply (brief, actionable steps)
5. Official link — use the EXACT Official URL string from the context data below. 
   Do NOT use markdown link syntax like [text](url). Just write the 
   bare URL on its own line exactly as provided in the context.

If no schemes match their situation, say so honestly and suggest 
they visit https://www.myscheme.gov.in directly.

LANGUAGE RULES (VERY IMPORTANT — follow strictly):
- Detect the language of the citizen's query below.
- If the citizen writes in ENGLISH, you MUST respond entirely in ENGLISH.
- If the citizen writes in HINDI (Devanagari script), respond in HINDI.
- If the citizen writes in HINGLISH (Hindi words in Roman/Latin script), 
  respond in HINGLISH.
- Default to ENGLISH if the language is unclear.

LINK RULES (VERY IMPORTANT):
- ONLY use URLs that appear in the context below. Never invent URLs.
- Write URLs as plain text, NOT as markdown links.
- Each scheme's URL should be on its own line.

Other rules:
- Never invent schemes not present in the context
- Never invent eligibility criteria
- NEVER invent or hallucinate numbers, amounts, or statistics. Only quote exact numbers if they are explicitly stated in the context.
- If unsure, say "you may qualify — please verify at the 
  official website"
- Always end with: "Please confirm your eligibility at the 
  official scheme website before applying."

Context:
{context}

Citizen's situation:
{question}
"""

def load_retriever():
    vectorstore = FAISS.load_local(
        "faiss_index", 
        EMBEDDINGS_MODEL,
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever(search_kwargs={"k": 8})

def get_qa_chain(retriever):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=SYSTEM_PROMPT
    )
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

def query_schemes(qa_chain, query: str):
    result = qa_chain.invoke({"query": query})
    answer = result["result"]
    
    # Build a map of all retrieved scheme names to URLs
    all_urls = {
        doc.metadata["name"]: doc.metadata["url"]
        for doc in result["source_documents"]
    }
    
    # Only include schemes the AI actually mentioned in the answer
    answer_lower = answer.lower()
    mentioned_sources = [
        name for name in all_urls.keys()
        if name.lower() in answer_lower
    ]
    
    # Build filtered URL map
    mentioned_urls = {
        name: all_urls[name]
        for name in mentioned_sources
    }
    
    return {
        "answer": answer,
        "sources": mentioned_sources,
        "source_urls": mentioned_urls
    }

