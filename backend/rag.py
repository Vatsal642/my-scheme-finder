from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
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

CRITICAL RULES (DO NOT IGNORE):
1. NO OUTSIDE KNOWLEDGE: You MUST ONLY suggest schemes that are explicitly provided in the `Context` block below. If a scheme is not in the context, DO NOT mention it.
2. NO FORCED MATCHES: You must strictly verify the citizen's demographics (age, gender, location, income). If the citizen is 28, DO NOT suggest adolescent schemes. If they are a farmer, DO NOT suggest student schemes.
3. RELIABILITY: Only suggest 1 or 2 highly reliable, exact matches. If you only find 1 exact match, suggest exactly 1.
4. ZERO MATCHES FALLBACK: If NO schemes in the provided context genuinely match their exact situation, you MUST output exactly this message and nothing else: "Sorry, I could not find any reliable matching schemes for your specific situation in my current database." Do NOT invent a scheme. Do NOT suggest Google searches.

FORMAT FOR EACH MATCH:
1. **Scheme name** (bold)
2. Why this person qualifies
3. Key benefit
4. How to apply
5. Official link — use the EXACT URL from the context data. If the context does not contain a URL for the scheme, provide a direct Google Search link for the exact scheme name (e.g., `https://www.google.com/search?q=[Exact+Scheme+Name]`). Do NOT use markdown link syntax like [text](url). Just write the bare URL on its own line.

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
    # Fetch top 15 to give the LLM a wider pool of relevant documents to choose from
    return vectorstore.as_retriever(search_kwargs={"k": 15})

def get_qa_chain(retriever):
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    # We return the raw components so we can orchestrate a multi-step LCEL pipeline in query_schemes
    return (retriever, llm)

def query_schemes(components, query: str):
    retriever, llm = components
    
    # Step 1: Query Expansion (Transform conversational query into clean keywords for FAISS)
    rewrite_prompt = PromptTemplate.from_template(
        "You are an expert search query generator. Extract the core keywords from this citizen's situation to query a vector database of government schemes. "
        "Ignore conversational filler like 'I am' or 'how to'. Extract ONLY the core demographic, location, income, and occupation. "
        "Output NOTHING ELSE but the keywords on a single line.\n"
        "Citizen query: {query}\nKeywords:"
    )
    clean_query = (rewrite_prompt | llm).invoke({"query": query}).content.strip()
    print(f"Original Query: {query} -> Expanded Query: {clean_query}")
    
    # Step 2: Fetch Documents
    docs = retriever.invoke(clean_query)
    
    # Step 3: Generate Answer
    context = "\n\n".join([f"Name: {d.metadata.get('name', 'Unknown')}\nDescription: {d.page_content}\nURL: {d.metadata.get('url', '')}" for d in docs])
    qa_prompt = PromptTemplate.from_template(SYSTEM_PROMPT)
    answer = (qa_prompt | llm).invoke({"context": context, "question": query}).content
    
    # Step 4: Map Source URLs
    all_urls = {
        d.metadata.get("name", "Unknown"): d.metadata.get("url", "")
        for d in docs
    }
    
    answer_lower = answer.lower()
    mentioned_sources = [
        name for name in all_urls.keys()
        if name.lower() in answer_lower
    ]
    
    mentioned_urls = {
        name: all_urls[name]
        for name in mentioned_sources
    }
    
    return {
        "answer": answer,
        "sources": mentioned_sources,
        "source_urls": mentioned_urls
    }
