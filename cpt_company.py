import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://day1cptuniversities.com/day-1-cpt/cpt-employers"

# --- Ensure ./data directory exists ---
os.makedirs("data", exist_ok=True)

# --- Fetch page ---
headers = {"User-Agent": "Mozilla/5.0 (compatible; Scraper/1.0)"}
r = requests.get(URL, headers=headers)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# --- Locate table ---
table = soup.find("table", {"id": "cei-summary-table"})
if not table:
    print("❌ Table with id='cei-summary-table' not found — page may be JS-rendered.")
else:
    # --- Convert to DataFrame ---
    df = pd.read_html(str(table))[0]
    df.columns = [c.strip().replace("\n", " ") for c in df.columns]
    print(f"✅ Extracted {len(df)} rows, {len(df.columns)} columns from CPT Employers")

    # --- Save to ./data/ folder ---
    output_path = os.path.join("data", "cpt_employers_day1cptuniversities_bs4.csv")
    df.to_csv(output_path, index=False)

    print(f"💾 Saved -> {output_path}")