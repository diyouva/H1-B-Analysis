# prepare.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob

try:
    from opt_company import get_opt_companies
except ImportError:
    get_opt_companies = None

try:
    from cpt_company import get_cpt_companies
except ImportError:
    get_cpt_companies = None


def detect_employer_column(df):
    """Detect which column represents the employer name."""
    for name in ["Employer", "Employer Name", "EMPLOYER_NAME", "EMPLOYER"]:
        if name in df.columns:
            return name
    raise ValueError("Employer column not found in H1B file.")


def load_and_clean(data_dir="data"):
    """Load and clean all H1B CSV files."""
    all_files = sorted(glob(os.path.join(data_dir, "h1b_datahubexport-*.csv")))
    dfs = []

    for f in all_files:
        year = int(os.path.basename(f).split("-")[-1].split(".")[0])
        df = pd.read_csv(f)

        # Standardize all column names early
        df.columns = df.columns.str.strip().str.replace(" ", "_")

        # Detect and rename employer column
        emp_col = None
        for name in ["Employer", "Employer_Name", "EMPLOYER", "EMPLOYER_NAME"]:
            if name in df.columns:
                emp_col = name
                break
        if emp_col is None:
            raise ValueError(f"Employer column not found in {f}")
        df.rename(columns={emp_col: "Employer"}, inplace=True)

        # Ensure numeric types for approval/denial columns
        for col in ["Initial_Approval", "Continuing_Approval",
                    "Initial_Denial", "Continuing_Denial"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            else:
                # fallback for unexpected column names (e.g., “Initial_Approvals”)
                alt = [c for c in df.columns if col.lower().replace("_", " ") in c.lower()]
                if alt:
                    df[col] = pd.to_numeric(df[alt[0]], errors="coerce").fillna(0)
                else:
                    df[col] = 0

        # Compute totals
        df["Total_Approvals"] = df["Initial_Approval"] + df["Continuing_Approval"]
        df["Total_Denials"] = df["Initial_Denial"] + df["Continuing_Denial"]
        df["Total_Applications"] = df["Total_Approvals"] + df["Total_Denials"]
        df["Year"] = year

        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    return df_all


def integrate_employers(df,
                        fortune_path="data/fortune500_opt_companies_2024.csv",
                        cpt_path="data/cpt_employers_day1cptuniversities_bs4.csv",
                        opt_path="data/opt_employers_scraped.csv"):
    """Integrate H1B data with Fortune500, OPT, and CPT employer lists.
       Use cached local files when available, otherwise scrape once and save."""
    
    # Fortune 500 dataset (always local)
    if os.path.exists(fortune_path):
        fortune = pd.read_csv(fortune_path)
        fortune["Employer_std"] = fortune["COMPANY NAME"].str.upper().str.strip()
        print("Loaded Fortune 500 data from local file.")
    else:
        raise FileNotFoundError("Fortune 500 file not found. Please provide it locally.")

    # OPT dataset
    if os.path.exists(opt_path):
        opt = pd.read_csv(opt_path)
        opt["Employer_std"] = opt["Employer_std"].str.upper().str.strip()
        print("Loaded OPT data from local file.")
    elif get_opt_companies:
        print("Scraping OPT employers (first time)...")
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
            cpt["CPT Friendly"] = cpt["CPT Friendly"].apply(lambda x: True if str(x).strip() == "✓" else False)
            cpt = cpt[cpt["CPT Friendly"]]
        print("Loaded CPT data from local file.")
    elif get_cpt_companies:
        print("Scraping CPT employers (first time)...")
        cpt = get_cpt_companies()
        cpt["Employer_std"] = cpt["Employer"].str.upper().str.strip()
        cpt.to_csv(cpt_path, index=False)
        print("CPT data saved for future runs.")
    else:
        cpt = pd.DataFrame(columns=["Employer_std"])

    # Standardize H1B employer names
    df["Employer_std"] = df["Employer"].str.upper().str.strip()

    # Boolean flags for category membership
    df["Fortune500"] = df["Employer_std"].isin(fortune["Employer_std"])
    df["OPT_friendly"] = df["Employer_std"].isin(opt["Employer_std"])
    df["CPT_friendly"] = df["Employer_std"].isin(cpt["Employer_std"])
    df["Flexibility_Index"] = df[["OPT_friendly", "CPT_friendly"]].sum(axis=1)

    total = len(df)
    f500 = df["Fortune500"].sum()
    opt_ct = df["OPT_friendly"].sum()
    cpt_ct = df["CPT_friendly"].sum()
    print(f"Integration completed for {total:,} employers:")
    print(f" - Fortune 500 matched: {f500:,}")
    print(f" - OPT friendly: {opt_ct:,}")
    print(f" - CPT friendly: {cpt_ct:,}")

    return df


def eda(df):
    """Generate quick exploratory data analysis plots."""
    plt.figure(figsize=(9, 5))
    sns.lineplot(data=df.groupby("Year")["Total_Approvals"].sum().reset_index(),
                 x="Year", y="Total_Approvals", marker="o")
    plt.title("H1B Approvals by Year")
    plt.tight_layout()
    plt.savefig("eda_trend.png")

    plt.figure(figsize=(6, 4))
    sns.barplot(data=df.groupby("Fortune500")["Total_Approvals"].sum().reset_index(),
                x="Fortune500", y="Total_Approvals")
    plt.title("Fortune 500 vs Non-Fortune 500 Approvals")
    plt.tight_layout()
    plt.savefig("eda_fortune.png")


if __name__ == "__main__":
    df = load_and_clean("data")
    df = integrate_employers(df)
    eda(df)
    df.to_csv("clean_h1b_data.csv", index=False)
    print("File clean_h1b_data.csv successfully saved.")