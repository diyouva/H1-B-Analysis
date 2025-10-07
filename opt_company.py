# unitedopt_super_stable.py
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Output directory setup ---
os.makedirs("data", exist_ok=True)

url = "https://www.unitedopt.com/Home/blogdetail/top-fortune-500-companies-offering-opt-jobs-to-international-students-in-2024"

# --- Chrome setup ---
options = Options()
# comment out the next line to see the browser window (useful for debugging)
# options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,3000")

driver = webdriver.Chrome(options=options)
driver.get(url)
print("🔹 Page opened. Waiting for table to load...")

# --- scroll to bottom to trigger lazy load ---
for i in range(10):
    driver.execute_script(f"window.scrollTo(0, {i*800});")
    time.sleep(1)

try:
    # Wait for the table element to be visible (not just present)
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "table.mrd-blog-table"))
    )
    print("✅ Table is visible.")
except Exception:
    print("⚠️ Table still not detected after waiting.")
    dump_path = os.path.join("data", "unitedopt_dump.html")
    with open(dump_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"💾 HTML dump saved → {dump_path}")
    driver.quit()
    raise SystemExit()

# --- Extract table HTML ---
table_html = driver.find_element(By.CSS_SELECTOR, "table.mrd-blog-table").get_attribute("outerHTML")
driver.quit()

# --- Parse HTML with BeautifulSoup + pandas ---
soup = BeautifulSoup(table_html, "html.parser")
table = soup.find("table")
df = pd.read_html(str(table))[0]
df.columns = [c.strip().replace("\n", " ") for c in df.columns]

# --- Save CSV inside ./data/ ---
output_path = os.path.join("data", "fortune500_opt_companies_2024.csv")
df.to_csv(output_path, index=False)

print(f"🎉 Successfully saved {len(df)} rows → {output_path}")