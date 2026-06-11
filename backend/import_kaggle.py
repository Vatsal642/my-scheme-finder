import csv
import json
import os

def import_csv(csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}.")
        print("Please ensure you downloaded the Kaggle CSV and renamed it to 'kaggle_schemes.csv' in the backend folder.")
        return

    schemes = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Lowercase keys to handle different CSV column names smoothly
            row_lower = {k.lower().strip() if k else '': v for k, v in row.items()}
            
            name = row_lower.get('scheme name', row_lower.get('scheme_name', row_lower.get('name', 'Unknown Scheme')))
            ministry = row_lower.get('ministry', row_lower.get('nodal ministry', row_lower.get('ministry_name', 'Various Ministries')))
            desc = row_lower.get('description', row_lower.get('brief', row_lower.get('details', '')))
            eligibility = row_lower.get('eligibility', row_lower.get('eligibility criteria', row_lower.get('eligibility_details', '')))
            benefits = row_lower.get('benefits', row_lower.get('scheme benefits', ''))
            how_to_apply = row_lower.get('application process', row_lower.get('how to apply', ''))
            state = row_lower.get('state', row_lower.get('state_name', 'All States'))
            
            if not name or name == 'Unknown Scheme':
                continue
                
            schemes.append({
                "name": name,
                "ministry": ministry,
                "description": desc,
                "eligibility": eligibility,
                "benefits": benefits,
                "how_to_apply": how_to_apply,
                "category": "General",
                "target_group": "General",
                "state": state,
                "url": f"https://www.myscheme.gov.in/search?q={name.replace(' ', '+')}"
            })

    print(f"✅ Successfully parsed {len(schemes)} schemes from CSV.")
    
    # Overwrite the schemes.json used by ingest.py
    out_path = "schemes.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(schemes, f, indent=2)
    print(f"✅ Saved correctly formatted data to {out_path}.")
    
    # Trigger the FAISS Vector DB rebuild
    print("⏳ Rebuilding FAISS vector database (this may take a few minutes for 3000+ schemes)...")
    exit_code = os.system("python3 ingest.py")
    
    if exit_code == 0:
        print("🎉 Database successfully updated! Please restart the backend server.")
    else:
        print("❌ Error during FAISS ingestion.")

if __name__ == "__main__":
    import_csv("kaggle_schemes.csv")
