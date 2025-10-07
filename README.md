
# International Students — H‑1B Policy Shock, OPT & CPT Pathways (Cohesive Version)

**Title:** Modeling Post‑Study Work Pathways — H‑1B, OPT, and CPT under Policy Shock  
**Author:** Diyouva C. Novith (Carnegie Mellon University, Heinz College)

## Run
```bash
pip install -r requirements.txt
python scripts/prepare_data.py
streamlit run app.py
```
(One-time scraping refresh, optional)
```bash
python scripts/scrape_data.py
```

## Data
Place the following files into `data/` (if you have them):
- `fortune500_opt_companies_2024.csv`  (OPT employers — UnitedOPT)
- `cpt_employers_day1cptuniversities_bs4.csv` (CPT-friendly employers — Day1CPT)
- `h1b_datahubexport-2015.csv` ... `h1b_datahubexport-2022.csv` (USCIS H-1B DataHub)

Derived outputs after `prepare_data.py`:
- `h1b_summary.csv`
- `employers_all_paths_scored.csv`

## Notes
- Scraping scripts are included but **not** auto-run in the app.
- Employer score combines OPT/CPT flags and H‑1B sponsor status.
