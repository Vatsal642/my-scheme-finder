from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional
import json, os
from dotenv import load_dotenv
load_dotenv()

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

from ingest import build_index
from rag import load_retriever, get_qa_chain, query_schemes
from scheduler import start_scheduler
from refresh import run_refresh

# Global state
retriever = None
qa_chain = None
scheduler_job = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global retriever, qa_chain, scheduler_job
    
    # Build index on first run if it doesn't exist
    if not os.path.exists("faiss_index"):
        print("No index found — building from scratch...")
        build_index()
    
    # Load retriever and QA chain
    try:
        retriever = load_retriever()
        qa_chain = get_qa_chain(retriever)
    except Exception as e:
        print(f"Failed to load retriever/chain: {e}")
    
    # Start weekly refresh scheduler
    scheduler_job = start_scheduler()
    
    print("App ready.")
    yield
    
    # Shutdown
    if scheduler_job:
        scheduler_job.shutdown()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    filters: Optional[dict] = {}

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

@app.post("/query")
def query(request: QueryRequest):
    if not qa_chain:
        raise HTTPException(status_code=503, detail="Model not ready")
    
    # Append filter context to query if provided
    enriched_query = request.query
    if request.filters:
        cat = request.filters.get("category")
        state = request.filters.get("state")
        if cat and cat != "all" and cat != "All Categories":
            enriched_query += f" Category: {cat}"
        if state and state != "all" and state != "All States":
            enriched_query += f" State: {state}"
    
    try:
        result = query_schemes(qa_chain, enriched_query)
    except Exception as e:
        print(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "source_urls": result["source_urls"],
        "query": request.query
    }

@app.get("/schemes")
async def get_schemes():
    if os.path.exists("schemes.json"):
        with open("schemes.json", "r", encoding="utf-8") as f:
            schemes = json.load(f)
        return [
            {
                "name": s["name"],
                "category": s.get("category", "general"),
                "target_group": s.get("target_group", ""),
                "ministry": s.get("ministry", ""),
                "url": s.get("url", "")
            }
            for s in schemes
        ]
    return []

@app.get("/last-updated")
async def last_updated():
    if os.path.exists("last_updated.json"):
        with open("last_updated.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "last_updated": "Not available",
        "scheme_count": 0,
        "source": "unknown"
    }

@app.post("/refresh")
async def manual_refresh():
    global retriever, qa_chain
    success = run_refresh()
    if success:
        try:
            retriever = load_retriever()
            qa_chain = get_qa_chain(retriever)
            return {"status": "success", "message": "Index refreshed"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Refresh succeeded but failed to load chain: {e}")
    raise HTTPException(status_code=500, detail="Refresh failed")

@app.get("/health")
async def health():
    return {"status": "ok"}
