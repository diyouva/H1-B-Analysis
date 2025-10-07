
# Modeling the Future of Post‑Study Work: Simulating the Policy Impact of a USD 100,000 H‑1B Filing Fee on OPT and CPT Pathways

**Author:** Diyouva C. Novith* (Carnegie Mellon University) — *Corresponding author*

## Abstract
Recent proposals to raise H‑1B filing fees to USD 100,000 introduce uncertainty in post‑study work. Integrating USCIS H‑1B (2015–2022) with scraped employer lists for OPT/CPT, author simulates cost elasticity and infer substitution effects. Results indicate a ~20% decline in H‑1B applications and 8–12% rise in OPT participation. Author discusses sectoral resilience and policy design.

## Introduction
The H‑1B pathway has historically bridged education and skilled employment. A steep fee increase risks altering incentives for employers and graduates alike. This project examines how the equilibrium among H‑1B, OPT, and CPT pathways may shift in response to a USD 100,000 filing fee. The contribution is twofold: an empirical integration of official and scraped sources, and a transparent “paper with code” workflow enabling full reproducibility.

## Literature Review
Prior work links skilled immigration to productivity and innovation. Recent studies show employer sensitivity to compliance costs and the growing importance of temporary authorizations (OPT, CPT) under tighter policies. Yet few combine official visa data with employer‑level lists for OPT and CPT; we address that gap.

## Methodology
Author collected USCIS H‑1B DataHub records (2015–2022) and scraped employer lists from UnitedOPT (OPT‑friendly Fortune 500) and Day‑1 CPT sources (CPT‑friendly employers). Employer names were normalized and deduplicated; descriptive trends and a cost‑elasticity simulation were used to model fee shocks. Outputs are implemented in Streamlit and packaged with Python scripts for data preparation and simulation.

### Example Code: Scraping (excerpt)
```python
from bs4 import BeautifulSoup
import requests, pandas as pd
URL = "https://www.unitedopt.com/..."
r = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})
soup = BeautifulSoup(r.text, "html.parser")
table = soup.find("table")
df_opt = pd.read_html(str(table))[0]
df_opt.to_csv("data/fortune500_opt_companies_2024.csv", index=False)
```

### Example Code: Simulation (excerpt)
```python
def simulate_h1b_cost_impact(base_apps, fee_usd, alpha=0.000002, opt_substitution=0.1):
    expected = max(base_apps * (1 - alpha*fee_usd), 0)
    opt_gain = max((base_apps - expected) * opt_substitution, 0)
    return expected, opt_gain
```

## Results and Discussion
Descriptive results show declining approval rates alongside persistent application volumes. Under the USD 100k scenario, H‑1B applications fall ~20%, with substitution into OPT/CPT concentrated in tech and finance. The employer‑overlap score demonstrates which firms sustain multi‑pathway hiring, guiding student job search and informing policy design.

## Conclusion
Raising H‑1B fees risks reorganizing the post‑study work ecosystem rather than reducing demand for talent. Balanced reforms—tiered fees, extended STEM‑OPT, strengthened cap‑exempt pathways—can maintain competitiveness while reducing unintended substitution.
