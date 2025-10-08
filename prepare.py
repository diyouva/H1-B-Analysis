# prepare.py
"""
PREPARE.PY
Data preparation script for:
"Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock"

Author: Diyouva C. Novith
Carnegie Mellon University, Heinz College of Information Systems and Public Policy

Purpose:
1. Load and standardize official USCIS H-1B DataHub files (2015–2023).
2. Integrate scraped or cached datasets for OPT- and CPT-friendly employers.
3. Produce a unified, analysis-ready dataset (clean_h1b_data.csv) for simulation and visualization.

This script reflects the empirical integration step described in the paper and policy brief,
creating a transparent link between the data sources and subsequent simulation analysis.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob

# Optional scraping utilities (only used if local caches do not exist)
try:
    from opt_company import get_opt_companies
except ImportError:
    get_opt_companies = None

try:
    from cpt_company import get_cpt_companies
except ImportError:
    get_cpt_companies = None


# ----------------------------------------------------------------------
# 1. Helper — Detect Employer Column
# ----------------------------------------------------------------------
def detect_employer_column(df):
    """Identify which column name represents the employer field."""
    for name in ["Employer", "Employer Name", "EMPLOYER_NAME", "EMPLOYER"]:
        if name in df.columns:
            return name
    raise ValueError("Employer column not found in H-1B dataset.")


# ----------------------------------------------------------------------
# 2. Load and Clean H-1B Datasets
# ----------------------------------------------------------------------
def load_and_clean(data_dir="data"):
    """
    Load all yearly H-1B CSV files (2015–2023), standardize headers,
    and calculate total approvals, denials, and applications.
    """
    all_files = sorted(glob(os.path.join(data_dir, "h1b_datahubexport-*.csv")))
    dfs = []

    for f in all_files:
        year = int(os.path.basename(f).split("-")[-1].split(".")[0])
        df = pd.read_csv(f)
        df.columns = df.columns.str.strip().str.replace(" ", "_")

        # Detect and rename employer column
        emp_col = detect_employer_column(df)
        df.rename(columns={emp_col: "Employer"}, inplace=True)

        # Normalize numeric fields
        for col in ["Initial_Approval", "Continuing_Approval",
                    "Initial_Denial", "Continuing_Denial"]:
            match = [c for c in df.columns if col.lower().replace("_", " ") in c.lower()]
            if match:
                df[col] = pd.to_numeric(df[match[0]], errors="coerce").fillna(0)
            else:
                df[col] = 0

        # Derived variables
        df["Total_Approvals"] = df["Initial_Approval"] + df["Continuing_Approval"]
        df["Total_Denials"] = df["Initial_Denial"] + df["Continuing_Denial"]
        df["Total_Applications"] = df["Total_Approvals"] + df["Total_Denials"]
        df["Year"] = year
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    print(f"Loaded {len(df_all):,} total H-1B records across {len(all_files)} years.")
    return df_all


# ----------------------------------------------------------------------
# 3. Integrate Employer Datasets (Fortune500, OPT, CPT)
# ----------------------------------------------------------------------
def integrate_employers(df,
                        fortune_path="data/fortune500_opt_companies_2024.csv",
                        opt_path="data/opt_employers_scraped.csv",
                        cpt_path="data/cpt_employers_day1cptuniversities_bs4.csv"):
    """
    Merge H-1B data with Fortune500, OPT, and CPT employer datasets.
    If local CSV files exist, they are used; otherwise, the script scrapes once and caches the results.
    """

    # Fortune 500 dataset
    fortune = pd.read_csv(fortune_path)
    fortune["Employer_std"] = fortune["COMPANY NAME"].str.upper().str.strip()
    print("Loaded Fortune 500 dataset.")

    # OPT dataset
    if os.path.exists(opt_path):
        opt = pd.read_csv(opt_path)
        opt["Employer_std"] = opt["Employer_std"].str.upper().str.strip()
        print("Loaded OPT data from local cache.")
    elif get_opt_companies:
        print("Scraping OPT data for the first time...")
        opt = get_opt_companies()
        opt["Employer_std"] = opt["Employer"].str.upper().str.strip()
        opt.to_csv(opt_path, index=False)
        print("OPT data saved for future runs.")
    else:
        opt = pd.DataFrame(columns=["Employer_std"])

    # CPT dataset
    if os.path.exists(cpt_path):
        cpt = pd.read_csv(cpt_path)
        cpt["Employer_std"] = cpt["Company"].str.upper().str.strip()
        if "CPT Friendly" in cpt.columns:
            cpt["CPT Friendly"] = cpt["CPT Friendly"].apply(lambda x: str(x).strip() == "✓")
            cpt = cpt[cpt["CPT Friendly"]]
        print("Loaded CPT data from local cache.")
    elif get_cpt_companies:
        print("Scraping CPT data for the first time...")
        cpt = get_cpt_companies()
        cpt["Employer_std"] = cpt["Employer"].str.upper().str.strip()
        cpt.to_csv(cpt_path, index=False)
        print("CPT data saved for future runs.")
    else:
        cpt = pd.DataFrame(columns=["Employer_std"])

    # Merge standardization
    df["Employer_std"] = df["Employer"].str.upper().str.strip()
    df["Fortune500"] = df["Employer_std"].isin(fortune["Employer_std"])
    df["OPT_friendly"] = df["Employer_std"].isin(opt["Employer_std"])
    df["CPT_friendly"] = df["Employer_std"].isin(cpt["Employer_std"])
    df["Flexibility_Index"] = df[["OPT_friendly", "CPT_friendly"]].sum(axis=1)

    print(f"Integration complete: {len(df):,} employer observations processed.")
    return df


# ----------------------------------------------------------------------
# 4. Exploratory Data Analysis (EDA)
# ----------------------------------------------------------------------
def eda(df):
    """Generate simple EDA charts illustrating temporal trends."""
    plt.figure(figsize=(9, 5))
    sns.lineplot(data=df.groupby("Year")["Total_Approvals"].sum().reset_index(),
                 x="Year", y="Total_Approvals", marker="o")
    plt.title("H-1B Approvals by Year")
    plt.tight_layout()
    plt.savefig("eda_trend.png")
    print("Saved trend plot as eda_trend.png.")


# ----------------------------------------------------------------------
# 5. Main Execution
# ----------------------------------------------------------------------
if __name__ == "__main__":
    df = load_and_clean("data")
    df = integrate_employers(df)
    eda(df)
    df.to_csv("clean_h1b_data.csv", index=False)
    print("clean_h1b_data.csv successfully saved.")