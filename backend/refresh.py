import shutil, os, json
from scraper import scrape_schemes
from ingest import build_index
from datetime import datetime

def run_refresh():
    print(f"[{datetime.now()}] Starting refresh...")
    try:
        # Step 1: scrape fresh data
        schemes = scrape_schemes()
        
        # Step 2: save to schemes.json
        if schemes:
            with open("schemes.json", "w", encoding="utf-8") as f:
                json.dump(schemes, f, indent=2)
        
        # Step 3: delete old FAISS index
        if os.path.exists("faiss_index"):
            shutil.rmtree("faiss_index")
        
        # Step 4: rebuild index
        build_index()
        
        # Step 5: write last_updated.json
        with open("last_updated.json", "w", encoding="utf-8") as f:
            json.dump({
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M IST"),
                "scheme_count": len(schemes) if schemes else 0,
                "source": "live"
            }, f)

        print(f"Refresh complete: {len(schemes) if schemes else 0} schemes indexed.")
        return True

    except Exception as e:
        print(f"Refresh failed: {e}")
        return False

if __name__ == "__main__":
    run_refresh()
