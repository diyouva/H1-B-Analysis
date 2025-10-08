# prepare.py
"""
PREPARE.PY
Data preparation script for:
"Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock"

Author: Diyouva C. Novith
Carnegie Mellon University, Heinz College of Information Systems and Public Policy

Purpose:
1. Load and standardize USCIS H-1B DataHub files (2015–2023).
2. Integrate Fortune500, OPT-, and CPT-friendly employer datasets.
3. Clean numeric columns to ensure correct plotting and aggregation.
4. Generate EDA charts and save them to /eda.
5. Save the cleaned dataset to /data/clean_h1b_data.csv.

Folders created automatically if missing.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob

# Optional scrapers (only used if local cache missing)
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
    """Detect which column represents the employer name."""
    for name in ["Employer", "Employer Name", "EMPLOYER_NAME", "EMPLOYER"]:
        if name in df.columns:
            return name
    raise ValueError("Employer column not found in H1B dataset.")


# ----------------------------------------------------------------------
# 2. Load and Clean H-1B Datasets
# ----------------------------------------------------------------------
def load_and_clean(data_dir="data"):
    """Load yearly H-1B CSV files, clean numeric fields, and compute totals."""
    all_files = sorted(glob(os.path.join(data_dir, "h1b_datahubexport-*.csv")))
    if not all_files:
        raise FileNotFoundError(f"No H-1B files found in {data_dir}/")

    dfs = []
    for f in all_files:
        year = int(os.path.basename(f).split("-")[-1].split(".")[0])
        df = pd.read_csv(f, dtype=str)
        df.columns = df.columns.str.strip().str.replace(" ", "_")

        emp_col = detect_employer_column(df)
        df.rename(columns={emp_col: "Employer"}, inplace=True)

        # Smart matching for numeric columns with flexible naming
        name_map = {
            "Initial_Approvals": ["Initial_Approval", "INITIAL_APPROVALS", "Initial Approvals"],
            "Continuing_Approvals": ["Continuing_Approval", "CONTINUING_APPROVALS", "Continuing Approvals"],
            "Initial_Denials": ["Initial_Denial", "INITIAL_DENIALS", "Initial Denials"],
            "Continuing_Denials": ["Continuing_Denial", "CONTINUING_DENIALS", "Continuing Denials"],
        }

        for target, aliases in name_map.items():
            found = None
            for alt in aliases:
                match = [c for c in df.columns if alt.lower().replace("_", "") in c.lower().replace("_", "")]
                if match:
                    found = match[0]
                    break

            if found:
                cleaned = (
                    df[found]
                    .astype(str)
                    .replace(r"[^0-9.\-]", "", regex=True)
                    .replace("", "0")
                )
                df[target] = pd.to_numeric(cleaned, errors="coerce").fillna(0)
            else:
                print(f"Warning: Column not found for {target} in {os.path.basename(f)}. Filled with zeros.")
                df[target] = 0

        # Compute totals
        df["Total_Approvals"] = df["Initial_Approvals"] + df["Continuing_Approvals"]
        df["Total_Denials"] = df["Initial_Denials"] + df["Continuing_Denials"]
        df["Total_Applications"] = df["Total_Approvals"] + df["Total_Denials"]
        df["Year"] = year
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)

    # Final numeric enforcement
    for col in ["Total_Approvals", "Total_Denials", "Total_Applications"]:
        df_all[col] = pd.to_numeric(df_all[col], errors="coerce").fillna(0).astype(int)

    print(f"Loaded {len(df_all):,} total H-1B records from {len(all_files)} files.")
    print("Example yearly totals:")
    print(df_all.groupby("Year")[["Total_Approvals", "Total_Denials", "Total_Applications"]].sum().head())

    return df_all


# ----------------------------------------------------------------------
# 3. Integrate Employer Datasets
# ----------------------------------------------------------------------
def integrate_employers(
    df,
    fortune_path="data/fortune500_opt_companies_2024.csv",
    opt_path="data/opt_employers_scraped.csv",
    cpt_path="data/cpt_employers_day1cptuniversities_bs4.csv",
):
    """Merge H-1B data with Fortune500, OPT, and CPT datasets."""
    # Fortune 500
    fortune = pd.read_csv(fortune_path)
    col = [c for c in fortune.columns if "COMPANY" in c.upper()][0]
    fortune["Employer_std"] = fortune[col].astype(str).str.upper().str.strip()
    print("Loaded Fortune 500 dataset.")

    # OPT dataset
    if os.path.exists(opt_path):
        opt = pd.read_csv(opt_path)
        if "Employer_std" not in opt.columns and "Employer" in opt.columns:
            opt["Employer_std"] = opt["Employer"]
        opt["Employer_std"] = opt["Employer_std"].astype(str).str.upper().str.strip()
        print("Loaded OPT dataset from local cache.")
    elif get_opt_companies:
        print("Scraping OPT data for the first time...")
        opt = get_opt_companies()
        opt["Employer_std"] = opt["Employer"].astype(str).str.upper().str.strip()
        opt.to_csv(opt_path, index=False)
        print("OPT data saved to cache.")
    else:
        opt = pd.DataFrame(columns=["Employer_std"])

    # CPT dataset
    if os.path.exists(cpt_path):
        cpt = pd.read_csv(cpt_path)
        if "Company" in cpt.columns:
            cpt["Employer_std"] = cpt["Company"].astype(str).str.upper().str.strip()
        else:
            cpt["Employer_std"] = cpt.iloc[:, 0].astype(str).str.upper().str.strip()

        if "CPT Friendly" in cpt.columns:
            cpt["CPT Friendly"] = cpt["CPT Friendly"].apply(lambda x: str(x).strip() == "✓")
            cpt = cpt[cpt["CPT Friendly"]]
        print("Loaded CPT dataset from local cache.")
    elif get_cpt_companies:
        print("Scraping CPT data for the first time...")
        cpt = get_cpt_companies()
        cpt["Employer_std"] = cpt["Employer"].astype(str).str.upper().str.strip()
        cpt.to_csv(cpt_path, index=False)
        print("CPT data saved to cache.")
    else:
        cpt = pd.DataFrame(columns=["Employer_std"])

    # Merge and standardize
    df["Employer_std"] = df["Employer"].astype(str).str.upper().str.strip()
    df["Fortune500"] = df["Employer_std"].isin(fortune["Employer_std"])
    df["OPT_friendly"] = df["Employer_std"].isin(opt["Employer_std"])
    df["CPT_friendly"] = df["Employer_std"].isin(cpt["Employer_std"])
    df["Flexibility_Index"] = df[["OPT_friendly", "CPT_friendly"]].sum(axis=1)

    print(f"Employer integration completed. Total records: {len(df):,}")
    return df


# ----------------------------------------------------------------------
# 4. Exploratory Data Analysis (save plots to /eda)
# ----------------------------------------------------------------------
def eda(df, output_dir="eda"):
    """Generate and save basic exploratory plots."""
    os.makedirs(output_dir, exist_ok=True)

    trend = df.groupby("Year")["Total_Approvals"].sum().reset_index()
    plt.figure(figsize=(9, 5))
    sns.lineplot(data=trend, x="Year", y="Total_Approvals", marker="o")
    plt.title("H-1B Approvals by Year")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "h1b_approvals_trend.png"))
    plt.close()

    comp = df.groupby("Fortune500")["Total_Approvals"].sum().reset_index()
    plt.figure(figsize=(6, 4))
    sns.barplot(data=comp, x="Fortune500", y="Total_Approvals")
    plt.title("Fortune 500 vs Non-Fortune 500 Approvals")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fortune500_comparison.png"))
    plt.close()

    print(f"EDA plots saved to: {output_dir}/")


# ----------------------------------------------------------------------
# 5. Main Execution
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Starting Data Preparation for H-1B / OPT / CPT Integration ===")

    # Step 1 — Load raw H-1B datasets
    df = load_and_clean("data")

    # Step 2 — Integrate employer datasets
    df = integrate_employers(df)

    # Step 3 — Generate EDA plots
    eda(df, output_dir="eda")

    # Step 4 — Save cleaned dataset to /data
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "clean_h1b_data.csv")
    df.to_csv(output_path, index=False)

    print(f"Dataset successfully saved to: {output_path}")
    print(f"Total records: {len(df):,}")
    print("=== Data preparation pipeline completed successfully ===")