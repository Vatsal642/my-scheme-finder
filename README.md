# Scheme Finder — AI-powered Government Scheme Eligibility Tool

## The Problem
India has 700+ government welfare schemes. Rs 1.7 lakh crore goes 
unclaimed every year — not because people don't need help, but 
because they can't find what they qualify for.

## The Solution
Describe yourself in plain English or Hindi. Scheme Finder retrieves 
the most relevant schemes from live government data and tells you 
exactly what you qualify for, what benefit you receive, and how to 
apply today.

## Why RAG and not just ChatGPT?
ChatGPT answers from its training memory — which may be outdated, 
hallucinated, or simply wrong for a specific scheme's eligibility 
criteria. This tool retrieves from the actual scheme data scraped 
from myscheme.gov.in, updated every week automatically. Every 
answer is grounded in a real source document. If the source doesn't 
say it, the tool doesn't say it.

## Auto-Update
The knowledge base refreshes every Sunday at 2am IST by scraping 
myscheme.gov.in. When the government announces a new scheme, it 
appears in the tool within 7 days — no manual work, no redeployment.

## Architecture
User Query → Next.js (Vercel)
          → FastAPI (Railway)
          → LangChain RetrievalQA
          → FAISS Vector Store
          → Google Generative AI Embeddings (retrieval)
          → gemini-1.5-flash (answer generation)
          → Answer + source scheme names → UI

## Tech Stack
| Layer       | Technology                    |
|-------------|-------------------------------|
| Frontend    | Next.js 14, TypeScript, Tailwind |
| Backend     | FastAPI, Python               |
| RAG         | LangChain, FAISS              |
| Embeddings  | Google Generative AI Embeddings |
| LLM         | gemini-1.5-flash                |
| Scraping    | httpx, BeautifulSoup4         |
| Scheduler   | APScheduler                   |
| Deploy      | Railway (backend) + Vercel (frontend) |

## Local Setup

Backend:
  ```bash
  cd backend
  pip install -r requirements.txt
  cp .env.example .env   # add your GOOGLE_API_KEY
  uvicorn main:app --reload
  ```

Frontend:
  ```bash
  cd frontend
  npm install
  cp .env.local.example .env.local   # add Railway URL
  npm run dev
  ```

## Adding a New Scheme Manually
Edit fallback_schemes.json, add the scheme dict, then hit 
POST /refresh — the index rebuilds automatically in ~30 seconds.

## Live Demo
[Add your Vercel URL here after deployment]
