import os
import json
import httpx
from bs4 import BeautifulSoup

def scrape_schemes():
    """
    Fetch all schemes from myscheme.gov.in.
    Returns a list of scheme dictionaries.
    """
    schemes = []
    
    # Step 1: try the official JSON API first
    api_url = "https://www.myscheme.gov.in/api/v1/schemes"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print("Attempting to fetch from API...")
    try:
        # In a real scenario, we would paginate. For now, try fetching page 1
        with httpx.Client() as client:
            response = client.get(api_url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                    for s in data["data"]:
                        schemes.append({
                            "name": s.get("name", ""),
                            "ministry": s.get("ministryName", ""),
                            "description": s.get("description", ""),
                            "eligibility": " ".join(s.get("eligibilityCriteria", [])),
                            "benefits": " ".join(s.get("benefits", [])),
                            "how_to_apply": s.get("applicationProcess", ""),
                            "category": s.get("tags", ["General"])[0] if s.get("tags") else "General",
                            "target_group": "General", # API might not provide target_group explicitly
                            "state": s.get("state", "All States"),
                            "url": s.get("schemeUrl", f"https://www.myscheme.gov.in/schemes/{s.get('slug', '')}")
                        })
                    
                    # Assume we have got all from API or a subset
                    if schemes:
                        print(f"Scraped {len(schemes)} schemes from live API.")
                        return schemes
    except Exception as e:
        print(f"Live scrape via API failed: {e}")

    # Step 2: if API fails, try HTML scrape (Placeholder logic)
    print("Attempting HTML scrape fallback...")
    html_url = "https://www.myscheme.gov.in/search"
    try:
        with httpx.Client() as client:
            resp = client.get(html_url, headers=headers, timeout=10.0)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                cards = soup.find_all("div", class_="scheme-card") # Hypothetical class
                if cards:
                    for card in cards:
                        name = card.find("h2").text.strip() if card.find("h2") else ""
                        if name:
                            slug = name.lower().replace(" ", "-")
                            schemes.append({
                                "name": name,
                                "ministry": "Unknown",
                                "description": card.find("p").text.strip() if card.find("p") else "",
                                "eligibility": "",
                                "benefits": "",
                                "how_to_apply": "",
                                "category": "General",
                                "target_group": "General",
                                "state": "All States",
                                "url": f"https://www.myscheme.gov.in/schemes/{slug}"
                            })
                    if schemes:
                        print(f"Scraped {len(schemes)} schemes from HTML.")
                        return schemes
    except Exception as e:
        print(f"Live HTML scrape failed: {e}")

    # Step 3: if both fail, load from fallback_schemes.json
    print("Live scrape failed — using fallback data.")
    fallback_path = os.path.join(os.path.dirname(__file__), "fallback_schemes.json")
    if os.path.exists(fallback_path):
        with open(fallback_path, "r", encoding="utf-8") as f:
            schemes = json.load(f)
            print(f"Loaded {len(schemes)} schemes from fallback.")
            return schemes
    
    print("No fallback data found.")
    return []

if __name__ == "__main__":
    scrape_schemes()
